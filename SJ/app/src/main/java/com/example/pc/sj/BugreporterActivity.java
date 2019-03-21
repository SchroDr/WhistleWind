package com.example.pc.sj;

import android.app.Activity;
import android.os.Bundle;
import android.os.Looper;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.Toast;

import java.io.IOException;

import okhttp3.Call;
import okhttp3.Callback;
import okhttp3.OkHttpClient;
import okhttp3.Response;

public class BugreporterActivity extends Activity implements View.OnClickListener, Callback {
    EditText bugMsg=null;
    Button submit=null;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.bug_reporter);
        submit=findViewById(R.id.bug_reporter_submit);
        bugMsg=findViewById(R.id.bug_reporter_msg);
        submit.setOnClickListener(this);
    }

    @Override
    public void onClick(View v) {
        String bug=bugMsg.getText().toString();
        if(bug.length()<3){
            Toast.makeText(this,"这也太短了吧,再多说几个字吧",Toast.LENGTH_LONG).show();
        }
        else {
            OkHttpClient okHttpClient=new OkHttpClient();
            Call call=okHttpClient.newCall(InternetConnector.getRequestForSendBug(bug));
            call.enqueue(this);
        }
    }

    @Override
    public void onFailure(Call call, IOException e) {
        Looper.prepare();
        Toast.makeText(this,"网络不畅,请稍后再试",Toast.LENGTH_LONG).show();
        Looper.loop();
    }

    @Override
    public void onResponse(Call call, Response response) throws IOException {
        Looper.prepare();
        Toast.makeText(this,"非常感谢您的支持",Toast.LENGTH_LONG).show();
        finish();
        Looper.loop();
    }
}
