package com.example.pc.sj;

import android.app.Activity;
import android.content.Context;
import android.graphics.Bitmap;
import android.widget.ImageView;

import java.util.ArrayList;

public class FreshImgView {
    public static void freshImgFromUrl(Activity c, ImageView iv, String url){
        new Thread(){
            public void run() {
                Bitmap bitmap=InternetConnector.getBitmapFromUrl(url);
                c.runOnUiThread(new Runnable() {
                    public void run() {
                        iv.setImageBitmap(bitmap);
                    }
                });
            }
        } .start();
    }
    public static void freshImgFromUrlAtOnce(Activity c, ImageView iv, String url){
        Bitmap bitmap=InternetConnector.getBitmapFromUrl(url);
        iv.setImageBitmap(bitmap);
    }
    public  static void freshImgs(Activity activity, ArrayList<ImageView> ivs,ArrayList<String> urls){

    }
}
