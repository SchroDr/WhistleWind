package com.example.pc.sj;

import android.app.Activity;
import android.content.Intent;
import android.os.Bundle;
import android.view.LayoutInflater;
import android.view.View;
import android.widget.LinearLayout;
import android.widget.Toast;

import com.suke.widget.SwitchButton;

import java.io.IOException;

import okhttp3.Call;
import okhttp3.Callback;
import okhttp3.OkHttpClient;
import okhttp3.Response;

public class FriendListActivity extends Activity implements View.OnClickListener, Callback {
    @Override
    protected void onCreate( Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.friend_list);
        LinearLayout friendListLinearLayout=findViewById(R.id.friend_list_content);
        OkHttpClient okHttpClient=new OkHttpClient();
        Intent intent=getIntent();
        String userId=intent.getStringExtra("userId");
        Call call=okHttpClient.newCall(InternetConnector.getRequestForGetFriendList(userId));
        for(int i=0;i<10;i++){
            View v=LayoutInflater.from(this).inflate(R.layout.friend_id_item,null);
            v.setOnClickListener(this);
            com.suke.widget.SwitchButton switchButton= v.findViewById(R.id.friend_id_item_switch_Btn);
            switchButton.setOnCheckedChangeListener(new SwitchButton.OnCheckedChangeListener() {
                @Override
                public void onCheckedChanged(SwitchButton view, boolean isChecked) {
                    if(isChecked){
                        Toast.makeText(FriendListActivity.this,"已关注",Toast.LENGTH_SHORT).show();
                    }
                    else
                        Toast.makeText(FriendListActivity.this,"已取消关注",Toast.LENGTH_SHORT).show();
                }
            });
            friendListLinearLayout.addView(v);
        }
    }

    @Override
    public void onClick(View v) {
        startActivity(new Intent(FriendListActivity.this,PersonalHomePageActivity.class));
    }

    @Override
    public void onFailure(Call call, IOException e) {

    }

    @Override
    public void onResponse(Call call, Response response) throws IOException {

    }
}
