package com.example.pc.sj;

import android.app.Activity;
import android.content.ClipboardManager;
import android.content.Context;
import android.content.Intent;
import android.content.SharedPreferences;
import android.os.Bundle;
import android.os.Looper;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.Toast;

import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

import java.io.IOException;
import java.util.HashMap;

import cn.pedant.SweetAlert.SweetAlertDialog;
import okhttp3.Call;
import okhttp3.Callback;
import okhttp3.FormBody;
import okhttp3.Headers;
import okhttp3.OkHttpClient;
import okhttp3.Request;
import okhttp3.RequestBody;
import okhttp3.Response;

public class LoginActivity extends Activity implements View.OnClickListener, Callback {
    EditText email=null;
    EditText password=null;
    Button confirm=null;
    public static final int Result_Code_Successful=11;
    @Override
    protected void onCreate( Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.login);
        email=findViewById(R.id.login_email);
        password=findViewById(R.id.login_password);
        confirm=findViewById(R.id.login_confirm);
        confirm.setOnClickListener(this);
        findViewById(R.id.login_forget).setOnClickListener(this);
        findViewById(R.id.register).setOnClickListener(this);

    }

    @Override
    public void onClick(View v) {
        int id=v.getId();
        if(id==R.id.login_confirm){
            if(email.getText().toString().equals("")){
                showToast("您还没有输入邮箱哦");
            }
            else if(password.getText().toString().equals("")){
                showToast("您还没有输入密码哦");
            }
            else {
                OkHttpClient okHttpClient = new OkHttpClient();
                HashMap<String,String> args=new HashMap<>();
                args.put("email",email.getText().toString());
                args.put("password",password.getText().toString());
                Call call=okHttpClient.newCall(InternetConnector.getRequestForLogin(args));
                call.enqueue(this);
            }
        }
        else if(id==R.id.login_forget){
            new SweetAlertDialog(this)
                    .setContentText("请使用您注册时的邮箱发送邮件至shunhu@aliyun.com申请更换密码哦~")
                    .setConfirmText("好吧")
                    .show();
            Toast.makeText(this,"邮箱已经在您的粘贴板里了,快去发送邮件吧",Toast.LENGTH_LONG).show();
            ClipboardManager clip = (ClipboardManager)getSystemService(Context.CLIPBOARD_SERVICE);
            String shareMsg="shunhu@aliyun.com";
            clip.setText(shareMsg);
        }
        else if(id==R.id.register){
            startActivity(new Intent(LoginActivity.this,RegisterActivity.class));
        }



    }

    @Override
    public void onFailure(Call call, IOException e) {
        Looper.prepare();
        Toast.makeText(this,"您的网络状况貌似不太好哦,请稍后再试",Toast.LENGTH_SHORT).show();
        e.printStackTrace();
        Looper.loop();
    }

    @Override
    public void onResponse(Call call, Response response) throws IOException {
        try {
            String json=response.body().string();
            JSONObject jsonObject=new JSONObject(json);
            String isSucceed=jsonObject.getString("isSucceed");
            String isNotExist=jsonObject.getString("isNotExist");
            String isWrong=jsonObject.getString("isWrong");
            String userId=jsonObject.getString("userId");
            Looper.prepare();
            if(isNotExist.equals("1")){
                showToast("用户不存在,你要不先注册一个?");
            }
            else if(isWrong.equals("1")){
                showToast("密码不对呀,好好想一想~");
            }
            else if(isSucceed.equals("0")){
                showToast("网络貌似出了点问题,一会再试试");
            }
            else {
                showToast("登录成功!");
                SharedPreferences shared=getSharedPreferences("share",MODE_PRIVATE);
                SharedPreferences.Editor editor=shared.edit();
                editor.putString("userId",userId);
                editor.commit();
                Intent intent=new Intent();
                intent.putExtra("userId",userId);
                setResult(Result_Code_Successful,intent);
                finish();
            }
            Looper.loop();
            //

        } catch (JSONException e) {
            e.printStackTrace();
        }


    }

    private void  showToast(String msg){

        Toast.makeText(this,msg,Toast.LENGTH_SHORT).show();

    }
}
