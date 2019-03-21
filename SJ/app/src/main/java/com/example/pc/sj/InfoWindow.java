package com.example.pc.sj;

import android.content.Context;
import android.util.Log;
import android.view.LayoutInflater;
import android.view.View;
import android.widget.Button;
import android.widget.LinearLayout;

import com.amap.api.maps.AMap;
import com.amap.api.maps.model.Marker;

public class InfoWindow implements AMap.InfoWindowAdapter,View.OnClickListener {
    private Context c=null;
    LinearLayout info_ll=null;
    public InfoWindow(Context c){
        this.c=c;
    }
    @Override
    public View getInfoWindow(Marker marker) {
        View infoWindowView=LayoutInflater.from(c).inflate(R.layout.info_window,null);
        Button likeBtn=infoWindowView.findViewById(R.id.like_button);
        Button dislikeBtn=infoWindowView.findViewById(R.id.dislike_button);
        Button commentBtn=infoWindowView.findViewById(R.id.comment_button);
        Button followBtn=infoWindowView.findViewById(R.id.follow_button);
        likeBtn.setOnClickListener(this);
        dislikeBtn.setOnClickListener(this);
        commentBtn.setOnClickListener(this);
        followBtn.setOnClickListener(this);
        return infoWindowView;
    }

    @Override
    public View getInfoContents(Marker marker) {
        return null;
    }

    @Override
    public void onClick(View v) {
        int id=v.getId();
        switch (id){
            case R.id.like_button:{
                //点赞
                Log.i("dianzan","233");
                break;
            }
            case R.id.dislike_button:{
                Log.i("laji","233");
                break;
            }
            case R.id.comment_button:{
                Log.i("pinlun","233");
                break;
            }
            case R.id.follow_button:{
                Log.i("zhuanfa","233");
                break;
            }
        }

    }
}
