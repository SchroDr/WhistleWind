package com.example.pc.sj;

import android.content.ContentResolver;
import android.content.Context;
import android.database.Cursor;
import android.graphics.Bitmap;
import android.graphics.BitmapFactory;
import android.net.Uri;
import android.os.Environment;
import android.provider.MediaStore;
import android.text.TextUtils;

import com.amap.api.maps.model.LatLng;

import java.io.File;
import java.io.FileNotFoundException;
import java.io.FileOutputStream;
import java.io.InputStream;
import java.net.HttpURLConnection;
import java.net.URL;
import java.util.ArrayList;
import java.util.List;
import java.util.Map;
import java.util.UUID;

import okhttp3.Call;
import okhttp3.FormBody;
import okhttp3.MediaType;
import okhttp3.MultipartBody;
import okhttp3.OkHttpClient;
import okhttp3.Request;
import okhttp3.RequestBody;

public  class  InternetConnector {
    public static final String Img_Head="http://lastation.me:8000/ww/getPic/?image_url=";
    public static final String Login="http://lastation.me:8000/ww/login/";//登录用url
    public static final String Quit="";//退出登录
    public static final String GetMsg="http://lastation.me:8000/ww/getMessages/";
    public static final String GetMsgDetial="http://lastation.me:8000/ww/getMsgInfo/";
    public static final String Like="";
    public static final String Dislike="";
    public static final String Follow="";//转发
    public static final String Comment="";
    public static final String SendMsg="http://lastation.me:8000/ww/postInfo/";
    public static final String UserDetial="";//打开用户详情页
    public static final String GetNotice="http://www.sliverp.cn/newnotice/";
    public static final String SendFile="http://www.sliverp.cn/newnotice/";
    public static final String Focus="";//关注用户
    public static final String DisFocus="";
    public static final String GetFriendList="http://www.sliverp.cn/newnotice/";
    public static final String SetUserHeaderImg="";//设置头像
    public static final String SetUserName="";
    public static final String Register="http://lastation.me:8000/ww/register/";
    public static final String BugReporter="http://www.sliverp.cn/bug";
    public static Bitmap getBitmapFromUrl(String url){
        Bitmap bmp = null;
        try {
            URL myurl = new URL(url);
            HttpURLConnection conn = (HttpURLConnection) myurl.openConnection();
            conn.setConnectTimeout(6000);//设置超时
            conn.setDoInput(true);
            conn.setUseCaches(false);//不缓存
            conn.connect();
            InputStream is = conn.getInputStream();//获得图片的数据流
            bmp = BitmapFactory.decodeStream(is);
            is.close();
        } catch (Exception e) {
            e.printStackTrace();
        }
        return bmp;
    }
    public static ArrayList<Bitmap> getBitmapArrayFromUrls(ArrayList<String> strings){
        ArrayList<Bitmap> bitmaps=new ArrayList<>();
        for(String s:strings){
            bitmaps.add(getBitmapFromUrl(s));
        }
        return bitmaps;
    }
    public static Request getRequestForNotice(){
        RequestBody requestBody=new FormBody.Builder()
                .add("NewNotice","NewNotice")
                .build();
        return getRequest(GetNotice,requestBody);
    }

    public static Request getRequestForComment(Context context,List<Uri> files){
        MultipartBody.Builder requestBodyBuilder=new MultipartBody.Builder()
                .addFormDataPart("msgId","456456465")
                .addFormDataPart("userId","123")
                .addFormDataPart("content","456")
                .setType(MultipartBody.FORM);
        if(files!=null)
            for(Uri file:files){
                requestBodyBuilder.addFormDataPart("file",
                        String.valueOf(file),
                        RequestBody.create(MediaType.parse("multipart/form-data"),
                                new File(UriUtils.getPath(context,file))));
            }
        RequestBody requestBody=requestBodyBuilder.build();
        Request request = new Request.Builder()
                .url(SendMsg)
                .post(requestBody)
                .build();
        return request;
    }

    public static Request getRequestForNewMsg(Map<String,String> args){
        RequestBody requestBody=getRequestbodyForFormbody(args);
        return getRequest(GetMsg,requestBody);
    }

    public static Request getRequestForLogin(Map<String,String> args){
        RequestBody requestBody=getRequestbodyForFormbody(args);
        return getRequest(Login,requestBody);
    }

    public static Request getRequestForGetMsgDetial(Map<String,String> args){
        RequestBody requestBody=getRequestbodyForFormbody(args);
        return getRequest(GetMsgDetial,requestBody);
    }

    public static Request getRequestForQuit(){
        RequestBody requestBody=new FormBody.Builder()
                .add("U","NewNotice")
                .build();
        return getRequest(Quit,requestBody);
    }

    public static Request getRequestForLike(){
        RequestBody requestBody=new FormBody.Builder()
                .add("NewNotice","NewNotice")
                .build();
        return getRequest(Like,requestBody);
    }
    public static Request getRequestForDislike(){
        RequestBody requestBody=new FormBody.Builder()
                .add("NewNotice","NewNotice")
                .build();
        return getRequest(Dislike,requestBody);
    }

    public static Request getRequestForGetFriendList(String userId){
        RequestBody requestBody=new FormBody.Builder()
                .add("userId",userId)
                .build();
        return getRequest(GetFriendList,requestBody);
    }

    public static Request getRequestForFollow(){
        RequestBody requestBody=new FormBody.Builder()
                .add("NewNotice","NewNotice")
                .build();
        return getRequest(Follow,requestBody);
    }
    public static Request getRequestForRegister(Map<String,String> args){
        RequestBody requestBody=getRequestbodyForFormbody(args);
        return getRequest(Register,requestBody);
    }

    public static Request getRequestForSendBug(String bugMsg){
        RequestBody requestBody=new FormBody.Builder()
                .add("bug",bugMsg)
                .build();
        return getRequest(BugReporter,requestBody);
    }

    public static Request getRequestForSendMsg(){
        RequestBody requestBody=new FormBody.Builder()
                .add("content","456456465")
                .add("userId","123")
                .add("x","0")
                .add("y","0")
                .build();
        return getRequest(SendMsg,requestBody);
    }
    public static Request getRequestForSendImg(List<Uri> files, Context context, String userId, String title, String content, LatLng latLng){
        MultipartBody.Builder requestBodyBuilder=new MultipartBody.Builder()
                .addFormDataPart("title",title)
                .addFormDataPart("content",content)
                .addFormDataPart("userID",userId)
                .addFormDataPart("x",String.valueOf(latLng.latitude))
                .addFormDataPart("y",String.valueOf(latLng.longitude))
                .setType(MultipartBody.FORM);
        if(files!=null)
            for(Uri file:files){
                //File bigImg=new File(UriUtils.getPath(context,file));
                File bigImg=new File(getRealFilePath(context,file));
                File smallImg=new File(bigImg.getParent()+"/"+userId+UserInfomation.getTime()+".jpg");
                try {
                    FileOutputStream outputStream=new FileOutputStream(smallImg);
                    Bitmap bigBp=BitmapFactory.decodeFile(bigImg.getAbsolutePath());
                    bigBp.compress(Bitmap.CompressFormat.JPEG,30,outputStream);
                } catch (FileNotFoundException e) {
                    e.printStackTrace();
                }
                requestBodyBuilder.addFormDataPart("img",
                        String.valueOf(smallImg),
                        RequestBody.create(MediaType.parse("multipart/form-data"),
                                smallImg));
            }
        RequestBody requestBody=requestBodyBuilder.build();
        Request request = new Request.Builder()
                .url(SendMsg)
                .post(requestBody)
                .build();
        return request;

    }
    private static Request getRequest(String url,RequestBody requestBody){
        return new Request.Builder().url(url).post(requestBody).build();
    }

    private static RequestBody getRequestbodyForFormbody( Map<String,String> args){
        FormBody.Builder builder=new FormBody.Builder();
        for(Map.Entry<String,String> arg:args.entrySet()){
            builder.add(arg.getKey(),arg.getValue());
        }
        return builder.build();
    }

    public static String getRealFilePath(Context context, Uri uri) {
        if (null == uri) return null;
        final String scheme = uri.getScheme();
        String realPath = null;
        if (scheme == null)
            realPath = uri.getPath();
        else if (ContentResolver.SCHEME_FILE.equals(scheme)) {
            realPath = uri.getPath();
        } else if (ContentResolver.SCHEME_CONTENT.equals(scheme)) {
            Cursor cursor = context.getContentResolver().query(uri,
                    new String[]{MediaStore.Images.ImageColumns.DATA},
                    null, null, null);
            if (null != cursor) {
                if (cursor.moveToFirst()) {
                    int index = cursor.getColumnIndex(MediaStore.Images.ImageColumns.DATA);
                    if (index > -1) {
                        realPath = cursor.getString(index);
                    }
                }
                cursor.close();
            }
        }
        if (TextUtils.isEmpty(realPath)) {
            if (uri != null) {
                String uriString = uri.toString();
                int index = uriString.lastIndexOf("/");
                String imageName = uriString.substring(index);
                File storageDir;

                storageDir = Environment.getExternalStoragePublicDirectory(
                        Environment.DIRECTORY_PICTURES);
                File file = new File(storageDir, imageName);
                if (file.exists()) {
                    realPath = file.getAbsolutePath();
                } else {
                    storageDir = context.getExternalFilesDir(Environment.DIRECTORY_PICTURES);
                    File file1 = new File(storageDir, imageName);
                    realPath = file1.getAbsolutePath();
                }
            }
        }
        return realPath;
    }


}
