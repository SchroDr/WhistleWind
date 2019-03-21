package com.example.pc.sj;

import android.Manifest;
import android.app.Activity;
import android.content.Intent;
import android.content.pm.ActivityInfo;
import android.content.pm.PackageManager;
import android.graphics.drawable.ColorDrawable;
import android.net.Uri;
import android.os.Build;
import android.os.Bundle;
import android.os.Looper;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.Toast;

import com.zhihu.matisse.Matisse;
import com.zhihu.matisse.MimeType;
import com.zhihu.matisse.engine.impl.GlideEngine;
import com.zhihu.matisse.internal.entity.CaptureStrategy;

import org.json.JSONException;
import org.json.JSONObject;

import java.io.IOException;
import java.util.ArrayList;
import java.util.List;
import java.util.concurrent.TimeUnit;

import cn.pedant.SweetAlert.SweetAlertDialog;
import okhttp3.Call;
import okhttp3.Callback;
import okhttp3.OkHttpClient;
import okhttp3.Response;

public class SendMsgActivity extends Activity implements View.OnClickListener {
    Button selectPictureBtn=null;
    Button atFriendBtn=null;
    Button emojiBtn=null;
    EditText title=null;
    EditText content=null;
    List<Uri> mSelected;
    public static  final int Send_Msg_Code=13;
    public static  final int From_Main_Activity=14;

    @Override
    protected void onCreate( Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.send_msg);
        selectPictureBtn=findViewById(R.id.send_msg_select_pic);
        atFriendBtn=findViewById(R.id.send_msg_at_friend);
        emojiBtn=findViewById(R.id.send_msg_emoji);
        findViewById(R.id.send_msg_cancel).setOnClickListener(this);
        findViewById(R.id.send_msg_send_btn).setOnClickListener(this);
        title=findViewById(R.id.send_msg_title);
        content=findViewById(R.id.send_msg_content);
        selectPictureBtn.setOnClickListener(this);
        atFriendBtn.setOnClickListener(this);
        emojiBtn.setOnClickListener(this);
    }

    //接受图片选择的结果
    @Override
    protected void onActivityResult(int requestCode, int resultCode, Intent data) {
        super.onActivityResult(requestCode, resultCode, data);
        if(data!=null){
            mSelected=Matisse.obtainResult(data);
            if(mSelected.size()!=0)
                selectPictureBtn.setText("已选择"+mSelected.size()+"张图片");
        }
    }

    @Override
    public void onClick(View v) {
        switch (v.getId()){
            case R.id.send_msg_select_pic:{
                Matisse.from(SendMsgActivity.this)
                        .choose(MimeType.allOf())//照片视频全部显示
                        .countable(true)//有序选择图片
                        .maxSelectable(9)//最大选择数量为9
                        .gridExpectedSize(400)//图片显示表格的大小
                        .restrictOrientation(ActivityInfo.SCREEN_ORIENTATION_PORTRAIT)//图像选择和预览活动所需的方向。
                        .thumbnailScale(0.85f)//缩放比例
                        .captureStrategy(//参数1 true表示拍照存储在共有目录，false表示存储在私有目录；参数2与 AndroidManifest中authorities值相同，用于适配7.0系统 必须设置
                                new CaptureStrategy(true, "com.example.pc.sj.fileprovider"))
                        .capture(true)//是否拍照
                        .theme(R.style.Matisse_Zhihu)//主题  暗色主题 R.style.Matisse_Dracula
                        .imageEngine(new GlideEngine())//加载方式
                        .forResult(22);//请求码
                break;
            }
            case R.id.send_msg_at_friend:{

                new SweetAlertDialog(this)
                        .setContentText("该功能还没有写哦")
                        .setConfirmText("那你加油哦")
                        .show();
                break;
            }
            case R.id.send_msg_emoji:{
                new SweetAlertDialog(this)
                        .setContentText("该功能还没有写哦")
                        .setConfirmText("那你加油哦")
                        .show();
                break;
            }
            case R.id.send_msg_cancel:{
                finish();
                break;
            }
            case R.id.send_msg_send_btn:{
                //startActivity(new Intent(SendMsgActivity.this,com.amap.searchdemo.MainActivity.class));
                if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O){
                    //没有定位权限
                    if(checkSelfPermission(Manifest.permission.ACCESS_FINE_LOCATION) == PackageManager.PERMISSION_GRANTED){
                        if(UserInfomation.isUserLocated(this)){//是否已成功被定位
                            sendMsg();
                        }
                        else {//没有被定位
                            Toast.makeText(this,"正在定位,请稍后再发送",Toast.LENGTH_LONG).show();
                        }
                    }
                    else {
                        Toast.makeText(this,"请您开放定位权限",Toast.LENGTH_LONG).show();
                        requestPermissions(new String[]{Manifest.permission.ACCESS_FINE_LOCATION},100);
                    }
                }
                else {
                    if(UserInfomation.isUserLocated(this)){//是否已成功被定位
                        sendMsg();
                    }
                    else {//没有被定位
                        Toast.makeText(this,"正在定位,请稍后再发送",Toast.LENGTH_LONG).show();
                    }
                }
            }
        }

    }
    public void sendMsg(){
        String userId=getIntent().getStringExtra("userId");
        String title_str=title.getText().toString();
        String content_str=content.getText().toString();
        if(content_str.length()<3){
            Toast.makeText(SendMsgActivity.this,"您的消息太短了,再多说两句吧",Toast.LENGTH_LONG).show();
        }
        else {
            OkHttpClient okHttpClient = new OkHttpClient.Builder()
                    .connectTimeout(10, TimeUnit.SECONDS)
                    .readTimeout(20, TimeUnit.SECONDS)
                    .build();
            Call call=okHttpClient.newCall(InternetConnector.getRequestForSendImg(mSelected,
                    this,userId,
                    title_str,
                    content_str,
                    UserInfomation.getUserLatlng(this)));
            SendMsg sendMsg=new SendMsg();

            call.enqueue(sendMsg);
            Toast.makeText(SendMsgActivity.this,"正在发送请稍后...",Toast.LENGTH_LONG).show();
            setResult(Send_Msg_Code);
            finish();
        }

    }
    class SendMsg implements Callback{

        @Override
        public void onFailure(Call call, IOException e) {
            e.printStackTrace();
            Looper.prepare();
            Toast.makeText(SendMsgActivity.this,"发送失败,请检查您的网络状况",Toast.LENGTH_LONG).show();
            Looper.loop();
        }

        @Override
        public void onResponse(Call call, Response response) throws IOException {
            try {
                String json=response.body().string();
                JSONObject jsonObject=new JSONObject(json);
                String name=jsonObject.getString("isSucceed");
                if(name.equals("1")){//发送成功
                    Looper.prepare();
                    Toast.makeText(SendMsgActivity.this,"发送成功",Toast.LENGTH_LONG).show();
                    Looper.loop();
                }
                else {//发送失败
                    Looper.prepare();
                    Toast.makeText(SendMsgActivity.this,"发送失败,请稍后再试",Toast.LENGTH_LONG).show();
                    Looper.loop();
                }
            } catch (JSONException e) {
                e.printStackTrace();
            }
        }
    }

}
