package com.example.pc.sj;

import android.app.Activity;
import android.content.Context;
import android.content.Intent;
import android.os.Bundle;
import android.os.Looper;
import android.util.Log;
import android.view.LayoutInflater;
import android.view.View;
import android.widget.Button;
import android.widget.ImageView;
import android.widget.LinearLayout;
import android.widget.TextView;
import android.widget.Toast;

import com.amap.api.maps.model.LatLng;
import com.awen.photo.FrescoImageLoader;
import com.awen.photo.photopick.controller.PhotoPagerConfig;
import com.zaaach.toprightmenu.MenuItem;
import com.zaaach.toprightmenu.TopRightMenu;

import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

import java.io.IOException;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;

import cn.pedant.SweetAlert.SweetAlertDialog;
import okhttp3.Call;
import okhttp3.Callback;
import okhttp3.OkHttpClient;
import okhttp3.Response;

public class DetailActivity extends Activity implements View.OnClickListener {
    ArrayList<ImageView> imageViews=null;
    Button like_btn=null;
    public JSONObject msgDetail=null;
    String name=null;
    String userId=null;
    String headerImgUrl=null;
    String title=null;
    String like=null;//点赞数
    String dislike=null;//点踩数
    String follow=null;//转发数
    String time=null;//信息发送时间
    ArrayList<String> commentsId=new ArrayList<>();
    @Override
    protected void onCreate( Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        OkHttpClient okHttpClient=new OkHttpClient();
        showLoadingPage();
        Intent intent=getIntent();
        HashMap<String,String> args=new HashMap<>();
        args.put("msgID",intent.getStringExtra("msgId"));
        Call call=okHttpClient.newCall(InternetConnector.getRequestForGetMsgDetial(args));
        call.enqueue(new GetMsgDetialResponse());
        FrescoImageLoader.init(this);
    }

    @Override
    public void onClick(View v) {
        int id=v.getId();
        if(id==R.id.datial_comment_imgView){//图片被点击,打开高清大图
            ArrayList<String> urls=new ArrayList<>();
            urls.add("http://i2.hdslb.com/bfs/archive/df77d8a9e3199df917cb6a68ffff2890059821d6.jpg");
            urls.add("http://i0.hdslb.com/bfs/album/caac18640a35f82bdcb724b073f07111da39d1bb.png");
            new PhotoPagerConfig.Builder(this)
                    .setBigImageUrls(urls)
                    .setSavaImage(true)
                    .build();

        }
        else if(id==R.id.detail_more_btn){
            //右上角的setting
            Log.i("dianl","ll");
            TopRightMenu topRightMenu=new TopRightMenu(this);
            List<MenuItem> menuItems=new ArrayList<>();
            menuItems.add(new MenuItem("分享"));
            menuItems.add(new MenuItem("举报"));
            topRightMenu.setHeight(250)
                    .setWidth(300)
                    .addMenuList(menuItems)
                    .setOnMenuItemClickListener(new TopRightMenu.OnMenuItemClickListener() {
                        @Override
                        public void onMenuItemClick(int position) {
                            switch (position){
                                case 0:{//分享按钮
//                                    new SweetAlertDialog(DetailActivity.this)
//                                            .setContentText("分享功能还没有写哦")
//                                            .setConfirmText("那你加油哦")
//                                            .show();
                                    Intent intent=new Intent(Intent.ACTION_SEND);
                                    intent.setType("*/*");
                                    intent.putExtra(Intent.EXTRA_SUBJECT, "Share");
                                    intent.putExtra(Intent.EXTRA_TEXT, "我正在使用[顺呼--社交2.0],点击下载:http://www.sliverp.cn 记得 QQ/微信 打开后在右上角选择用浏览器打开哦");
                                    intent.setFlags(Intent.FLAG_ACTIVITY_NEW_TASK);
                                    startActivity(Intent.createChooser(intent, "分享到"));
                                    break;
                                }
                                case 1:{//举报按钮,还没有发请求
                                    Toast.makeText(DetailActivity.this,"举报成功",Toast.LENGTH_LONG).show();
                                    break;
                                }
                            }
                        }
                    }).showAsDropDown(v);
        }
        else if(id==R.id.detail_like_button){//点赞按钮
            try {
                OkHttpClient okHttpClient=new OkHttpClient();
                Call call=okHttpClient.newCall(InternetConnector.getRequestForLike());
                call.execute();
                int currentLikeNum=Integer.parseInt(like_btn.getText().toString());
                like_btn.setText(""+(currentLikeNum+1));
            } catch (IOException e) {
                e.printStackTrace();
            }
        }
        else if(id==R.id.detail_dislike_button){//点垃圾
            try {
                OkHttpClient okHttpClient=new OkHttpClient();
                Call call=okHttpClient.newCall(InternetConnector.getRequestForDislike());
                call.execute();
            } catch (IOException e) {
                e.printStackTrace();
            }
        }
        else if(id==R.id.detail_follow_button){//转发
                OkHttpClient okHttpClient=new OkHttpClient();
                Call call=okHttpClient.newCall(InternetConnector.getRequestForFollow());
                call.enqueue(new FollowResponse());
        }

        else {
            new SweetAlertDialog(this)
                    .setContentText("该功能还没有写哦")
                    .setConfirmText("那你加油哦")
                    .show();
        }

    }

    class BigImgOnClickListener implements View.OnClickListener{
        ArrayList<String> imgUrls=null;
        public BigImgOnClickListener(ArrayList<String> imgUrls){
            this.imgUrls=imgUrls;
        }
        @Override
        public void onClick(View v) {
            new PhotoPagerConfig.Builder(DetailActivity.this)
                    .setBigImageUrls(imgUrls)
                    .setSavaImage(true)
                    .build();
        }
    }

    public void showLoadingPage(){//接受信息时显示
        setContentView(R.layout.loading);
    }

    public void showLoadedPage(){//信息加载结束
        setContentView(R.layout.detail);
        Intent intent=getIntent();
        String code=intent.getStringExtra("msgId");
        imageViews=new ArrayList<>();
        ArrayList<String> imgUrls=(ArrayList<String>)getIntent().getSerializableExtra("imgUrls");
        BigImgOnClickListener bigImgOnClickListener=new BigImgOnClickListener(imgUrls);
        //根据url个数添加img
        for(String imgUrl:imgUrls){
            ImageView iv=new ImageView(this);
            iv.setOnClickListener(bigImgOnClickListener);
            FreshImgView.freshImgFromUrl(this,iv,imgUrl);
            imageViews.add(iv);

        }
        LinearLayout imgArea=findViewById(R.id.detail_img_field);
        for(ImageView i:imageViews)
            imgArea.addView(i);
//        ImageView iv=findViewById(R.id.datial_imgView);
//        FreshImgView.freshImgFromUrl(this,iv,intent.getStringExtra("imgUrl"));
        // ImageView imageView;


        // iv.setOnClickListener(this);
        TextView title_TV=findViewById(R.id.datial_title);
        this.like_btn=findViewById(R.id.detail_like_button);
        like_btn.setOnClickListener(this);
        findViewById(R.id.detail_dislike_button).setOnClickListener(this);
        findViewById(R.id.detail_follow_button).setOnClickListener(this);
        findViewById(R.id.detail_comment_button).setOnClickListener(this);
        findViewById(R.id.detail_more_btn).setOnClickListener(this);
        title_TV.setText(code);
        LinearLayout commentArea=findViewById(R.id.datial_comment_area);
//        for(int i=1;i<5;i++){
//            View commentView =LayoutInflater.from(this).inflate(R.layout.datile_comment, null);
//            commentView.findViewById(R.id.datial_comment_head).setOnClickListener(this);
//            commentView.findViewById(R.id.datial_comment_name).setOnClickListener(this);
//            commentView.findViewById(R.id.datial_comment_like_btn).setOnClickListener(this);
//            ImageView imageView=commentView.findViewById(R.id.datial_comment_imgView);
//        FreshImgView.freshImgFromUrl(this,imageView,intent.getStringExtra("imgUrl"));
//            imageView.setOnClickListener(this);
//            commentArea.addView(commentView);
//        }
    }

    public void showLoadedFailPage(){
        setContentView(R.layout.loaded_fail);
    }

    class FollowResponse implements Callback{
        @Override
        public void onFailure(Call call, IOException e) {
            Looper.prepare();
            Toast.makeText(DetailActivity.this,"转发失败,请稍后再试",Toast.LENGTH_LONG).show();
            Looper.loop();
        }

        @Override
        public void onResponse(Call call, Response response) throws IOException {
            Looper.prepare();
            Toast.makeText(DetailActivity.this,"转发成功",Toast.LENGTH_LONG).show();
            Looper.loop();
        }
    }

    class  GetMsgDetialResponse implements Callback{

        @Override
        public void onFailure(Call call, IOException e) {
            runOnUiThread(new Runnable() {
                @Override
                public void run() {
                    showLoadedFailPage();
                }
            });
        }

        @Override
        public void onResponse(Call call, Response response) throws IOException {
            try {
                String json=response.body().string();
                msgDetail=new JSONObject(json);
                name=msgDetail.getString("name");
                userId=msgDetail.getString("userID");
                //title=msgDetail.getString("title");
                title="title";
                headerImgUrl=msgDetail.getString("headerImgUrl");
                like=msgDetail.getString("like");
                dislike=msgDetail.getString("dislike");
               // follow=msgDetail.getString("follow");
                time=msgDetail.getString("time");
                JSONArray comments=new JSONArray(msgDetail.getString("comments"));
                for(int i=0;i<comments.length();i++){
                    commentsId.add(comments.getString(i));
                }

                runOnUiThread(new Runnable() {
                    @Override
                    public void run() {
                        showLoadedPage();
                    }
                });
            } catch (Exception e) {
                e.printStackTrace();
            }

        }
    }

    class GetCommentsResponse implements Callback{

        @Override
        public void onFailure(Call call, IOException e) {

        }

        @Override
        public void onResponse(Call call, Response response) throws IOException {

        }
    }
}

