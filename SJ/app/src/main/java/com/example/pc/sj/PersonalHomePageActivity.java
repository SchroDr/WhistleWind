package com.example.pc.sj;

import android.app.Activity;
import android.content.Intent;
import android.graphics.BitmapFactory;
import android.os.Bundle;
import android.util.AttributeSet;
import android.view.LayoutInflater;
import android.view.View;
import android.widget.ImageView;
import android.widget.LinearLayout;
import android.widget.TextView;

import com.amap.api.maps.MapView;

import org.apmem.tools.layouts.FlowLayout;

public class PersonalHomePageActivity extends Activity implements View.OnClickListener {
    LinearLayout personalMsgs=null;
    @Override
    protected void onCreate( Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.home_page);
        Intent intent=getIntent();
        personalMsgs=findViewById(R.id.home_page_content);
        for(int i=0;i<10;i++){
            View v=LayoutInflater.from(this).inflate(R.layout.personal_msg,null);
            TextView textView=v.findViewById(R.id.personal_msg_content);
            textView.setText("deeeeeeeeeeeeeeeeeee");
            FlowLayout flowLayout=v.findViewById(R.id.personal_msg_img_field);
            ImageView imageView=new ImageView(this);
            flowLayout.addView(imageView);
           // imageView.setImageBitmap(BitmapFactory.decodeFile("@mi"));
            FreshImgView.freshImgFromUrl(this,imageView,"http://i2.hdslb.com/bfs/archive/df77d8a9e3199df917cb6a68ffff2890059821d6.jpg");
            personalMsgs.addView(v);
        }
    }

    @Override
    public void onClick(View v) {

    }
}
