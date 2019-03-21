package com.example.pc.sj;

import android.app.Activity;
import android.content.Context;
import android.graphics.Bitmap;
import android.graphics.Point;
import android.view.LayoutInflater;
import android.view.View;
import android.widget.ImageView;
import android.widget.TextView;

import com.amap.api.maps.AMap;
import com.amap.api.maps.model.BitmapDescriptor;
import com.amap.api.maps.model.BitmapDescriptorFactory;
import com.amap.api.maps.model.LatLng;
import com.amap.api.maps.model.MarkerOptions;

public class Msg  {
    public MarkerOptions markerOption=null;
    AMap aMap=null;
    LatLng latLng=null;
    View v=null;
    TextView textView=null;
    Context c=null;
    Msg(Context c, LatLng latLng, AMap aMap, Bitmap bitmap){
        markerOption = new MarkerOptions();
        this.latLng=latLng;
        this.aMap=aMap;
        this.c=c;
        BitmapDescriptor b=BitmapDescriptorFactory.fromView(getMsgView(c,bitmap));
        markerOption.position(latLng);
        markerOption.icon(b);
        markerOption.snippet("线索");
    }
    Msg(Context c,AMap aMap, MsgInfo msgInfo){
        markerOption = new MarkerOptions();
        this.latLng=msgInfo.latLng;
        this.aMap=aMap;
        this.c=c;
        BitmapDescriptor b=BitmapDescriptorFactory.fromView(getMsgView(c,msgInfo));
        markerOption.position(latLng);
        markerOption.icon(b);
    }
    public View getMsgView(Context c,Bitmap bitmap){
        //LayoutInflater inflater = (LayoutInflater)c.getSystemService(Context.LAYOUT_INFLATER_SERVICE);
        v=LayoutInflater.from(c).inflate(R.layout.info, null);
        textView=v.findViewById(R.id.msg_content);
        ImageView imageView=v.findViewById(R.id.msg_img);
        imageView.setImageBitmap(bitmap);
       // FreshImgView.freshImgFromUrl((Activity)c,imageView,"http://i2.hdslb.com/bfs/archive/df77d8a9e3199df917cb6a68ffff2890059821d6.jpg");
        Point point=aMap.getProjection().toScreenLocation(this.latLng);
        String s="x="+point.x+",y="+point.y;
        textView.setText(s.toCharArray(),0,s.length());
        return  v;
    }
    public View getMsgView(Context c,MsgInfo msgInfo){
        v=LayoutInflater.from(c).inflate(R.layout.info, null);
        TextView title=v.findViewById(R.id.msg_title);
        title.setText(msgInfo.title);
        textView=v.findViewById(R.id.msg_content);
        textView.setText(msgInfo.content);
        ImageView imageView=v.findViewById(R.id.msg_img);
        imageView.setImageBitmap(msgInfo.bitmap);
        return  v;
    }

    public void setPos(LatLng latLng){
        markerOption.position(latLng);
    }
    public MarkerOptions getMarkerOption(){
        return this.markerOption;
    }
    public void setContent(String s){
        v=LayoutInflater.from(c).inflate(R.layout.info, null);
        textView=v.findViewById(R.id.msg_content);
        textView.setText(s.toCharArray(),0,s.length());

    }
    public void freshContent(){
        Point point=aMap.getProjection().toScreenLocation(this.latLng);
        setContent("x="+point.x+",y="+point.y);
        BitmapDescriptor b=BitmapDescriptorFactory.fromView(v);
        markerOption.icon(b);


    }
}
