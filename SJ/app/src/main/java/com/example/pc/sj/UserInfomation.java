package com.example.pc.sj;

import android.app.Activity;
import android.content.Context;
import android.content.SharedPreferences;

import com.amap.api.maps.model.LatLng;

import java.util.Date;

public class UserInfomation {
   public static String getUserId(Activity activity){
        SharedPreferences sharedPreferences=activity.getSharedPreferences("share",Context.MODE_PRIVATE);
        return sharedPreferences.getString("userId","");
   }
   public static boolean isLogin(Activity activity){
       SharedPreferences sharedPreferences=activity.getSharedPreferences("share",Context.MODE_PRIVATE);
       return !sharedPreferences.getString("userId","").equals("");
   }
   public static LatLng getUserLatlng(Activity activity){
       SharedPreferences sharedPreferences=activity.getSharedPreferences("share",Context.MODE_PRIVATE);
       return new LatLng(Double.valueOf(sharedPreferences.getString("x","")),Double.valueOf(sharedPreferences.getString("y","")));
   }

   public static boolean isUserLocated(Activity activity){
       SharedPreferences sharedPreferences=activity.getSharedPreferences("share",Context.MODE_PRIVATE);
       return sharedPreferences.getString("isLocation","").equals("1");
   }
   public static String getX(Activity activity){
       SharedPreferences sharedPreferences=activity.getSharedPreferences("share",Context.MODE_PRIVATE);
       return sharedPreferences.getString("x","");
   }

    public static String getY(Activity activity){
        SharedPreferences sharedPreferences=activity.getSharedPreferences("share",Context.MODE_PRIVATE);
        return sharedPreferences.getString("y","");
    }
    public static String getTime(){
        Date date=new Date();
        return date.getTime()+"";
    }
}
