package com.example.pc.sj;

import android.app.Activity;
import android.content.Intent;
import android.os.Bundle;
import android.view.View;
import android.widget.ImageView;

public class ImgBrowseActivity extends Activity implements View.OnClickListener,View.OnLongClickListener {
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.img_browse);
        Intent intent=getIntent();
        ImageView imageView=findViewById(R.id.img_browse_imgView);
        imageView.setOnClickListener(this);
        imageView.setOnLongClickListener(this);
    }

    @Override
    public void onClick(View v) {
        finish();
    }

    @Override
    public boolean onLongClick(View v) {//长按图片的逻辑
        return false;
    }
}
