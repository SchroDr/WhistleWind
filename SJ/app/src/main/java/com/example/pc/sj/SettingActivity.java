package com.example.pc.sj;

import android.app.Activity;
import android.content.Intent;
import android.os.Bundle;
import android.view.View;

public class SettingActivity extends Activity implements View.OnClickListener {
    @Override
    protected void onCreate( Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.setting);
        findViewById(R.id.setting_account).setOnClickListener(this);
        findViewById(R.id.setting_notice).setOnClickListener(this);
        findViewById(R.id.setting_general).setOnClickListener(this);
        findViewById(R.id.setting_about).setOnClickListener(this);

    }

    @Override
    public void onClick(View v) {
        int id=v.getId();
        if(id==R.id.setting_account){
            startActivity(new Intent(SettingActivity.this,AccountSettingActivity.class));
            //账户设置
        }
        else if(id==R.id.setting_general){
            //通用设置
        }
        else if(id==R.id.setting_notice){
            startActivity(new Intent(SettingActivity.this,NoticeSettingActivity.class));
            //通知设置
        }
        else if(id==R.id.setting_about){
            //关于
            startActivity(new Intent(SettingActivity.this,AboutSettingActivity.class));
        }
    }
}
