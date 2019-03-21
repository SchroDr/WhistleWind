package com.example.pc.sj;

import android.app.Activity;
import android.os.Bundle;
import android.os.Looper;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.Toast;

import org.json.JSONException;
import org.json.JSONObject;

import java.io.IOException;
import java.util.HashMap;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

import okhttp3.Call;
import okhttp3.Callback;
import okhttp3.OkHttpClient;
import okhttp3.Response;

public class RegisterActivity extends Activity implements View.OnClickListener, Callback {
    EditText email=null;
    EditText password=null;
    EditText repassword=null;
    Button confirm=null;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.register);
        email=findViewById(R.id.register_email);
        password=findViewById(R.id.register_password);
        repassword=findViewById(R.id.register_repassword);
        confirm=findViewById(R.id.register_confirm);
        confirm.setOnClickListener(this);
    }

    @Override
    public void onClick(View v) {
        String email_str=email.getText().toString();
        String password_str=password.getText().toString();
        String repassword_str=repassword.getText().toString();
        if(email_str.equals("")){
            email.setError("你还没有输入邮箱呢");
        }
        else if(password_str.equals("")){
            password.setError("请输入密码哦~");
        }
        else if(repassword_str.equals("")){
            repassword.setError("请再次输入密码哦~");
        }
        else if(!password_str.equals(repassword_str)){
            repassword.setError("前后密码不一致哦~");
        }
        else if(!email_str.matches("\\w+([-+.]\\w+)*@\\w+([-.]\\w+)*\\.\\w+([-.]\\w+)*")){
            email.setError("请正确输入邮箱哦");
        }
        else{

            OkHttpClient okHttpClient=new OkHttpClient();
            HashMap<String,String> args=new HashMap<>();
            args.put("email",email_str);
            args.put("password",password_str);
            Call call =okHttpClient.newCall(InternetConnector.getRequestForRegister(args));
            call.enqueue(this);
        }

    }

    @Override
    public void onFailure(Call call, IOException e) {
        Toast.makeText(this,"您的网络状况貌似不太好哦,请稍后再试",Toast.LENGTH_LONG).show();
    }

    @Override
    public void onResponse(Call call, Response response) throws IOException {

        try {
            String res=response.body().string();
            JSONObject jsonObject= new JSONObject(res);
            String isSucceed=jsonObject.getString("isSucceed");
            String isExist=jsonObject.getString("isExist");
            if(isExist.equals("1")){
                Looper.prepare();
                Toast.makeText(this,"该邮箱已经被注册了哦~换一个试试吧",Toast.LENGTH_LONG).show();
                Looper.loop();
            }
            else if(isSucceed.equals("0")){
                Looper.prepare();
                Toast.makeText(this,"网络不畅,请稍后再试~",Toast.LENGTH_LONG).show();
                Looper.loop();
            }
            else {
                Looper.prepare();
                Toast.makeText(this,"注册成功~",Toast.LENGTH_LONG).show();
                finish();
                Looper.loop();
            }
        } catch (JSONException e) {
            e.printStackTrace();
        }

    }
}
//验证是不是邮箱
 class RegExpValidator {

    public static boolean isEmail( String str ) {
        String regex = "[a-zA-Z_]{1,}[0-9]{0,}@(([a-zA-z0-9]-*){1,}\\.){1,3}[a-zA-z\\-]{1,}" ;
        return match( regex ,str );
    }

    public static boolean isHomepage( String str ){
        String regex = "http://(([a-zA-z0-9]|-){1,}\\.){1,}[a-zA-z0-9]{1,}-*" ;
        return match( regex ,str );
    }

    private static boolean match( String regex ,String str ){
        Pattern pattern = Pattern.compile(regex);
        Matcher matcher = pattern.matcher( str );
        return matcher.matches();
    }

}
