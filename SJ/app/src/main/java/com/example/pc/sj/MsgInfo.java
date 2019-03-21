package com.example.pc.sj;


import android.app.Activity;
import android.content.Context;
import android.graphics.Bitmap;

import com.amap.api.maps.model.LatLng;

import java.util.ArrayList;

public class MsgInfo {
    public Activity c=null;
    public LatLng latLng=new LatLng(39.906901,116.397972);
    public String title="nbnbnb";
    public String content="nbnbnbnb";
    public String msgId="14725839";
    public String time="11:31";
    public String imgUrl="http://lastation.me:8000/ww/getPic/?image_url=media/avatars/rua.jpg";
    public ArrayList<String> imgUrls=new ArrayList<>();
    public Bitmap bitmap=null;
    public MsgInfo(){

    }
}
