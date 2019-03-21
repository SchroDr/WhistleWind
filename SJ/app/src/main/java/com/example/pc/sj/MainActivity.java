package com.example.pc.sj;

import android.Manifest;
import android.app.Activity;
import android.app.Notification;
import android.app.NotificationChannel;
import android.app.NotificationManager;
import android.content.ClipboardManager;
import android.content.Context;
import android.content.Intent;
import android.content.SharedPreferences;
import android.content.pm.PackageInfo;
import android.content.pm.PackageManager;
import android.graphics.Bitmap;
import android.graphics.Point;
import android.os.Build;
import android.os.Bundle;
import android.os.Looper;
import android.support.annotation.Nullable;
import android.support.annotation.RequiresApi;
import android.util.Log;
import android.view.View;
import android.support.design.widget.NavigationView;
import android.support.v4.view.GravityCompat;
import android.support.v4.widget.DrawerLayout;
import android.support.v7.app.ActionBarDrawerToggle;
import android.support.v7.app.AppCompatActivity;
import android.support.v7.widget.Toolbar;
import android.view.Menu;
import android.view.MenuItem;
import android.widget.Button;
import android.widget.TextView;
import android.widget.Toast;

import com.amap.api.location.AMapLocation;
import com.amap.api.location.AMapLocationClient;
import com.amap.api.location.AMapLocationClientOption;
import com.amap.api.location.AMapLocationListener;
import com.amap.api.maps.AMap;
import com.amap.api.maps.AMapUtils;
import com.amap.api.maps.CameraUpdateFactory;
import com.amap.api.maps.MapView;
import com.amap.api.maps.Projection;
import com.amap.api.maps.UiSettings;
import com.amap.api.maps.model.LatLng;
import com.amap.api.maps.model.Marker;

import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

import java.io.IOException;
import java.security.MessageDigest;
import java.security.NoSuchAlgorithmException;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.Locale;
import java.util.Map;

import cn.pedant.SweetAlert.SweetAlertDialog;
import okhttp3.Call;
import okhttp3.Callback;
import okhttp3.OkHttpClient;
import okhttp3.Response;

public class MainActivity extends AppCompatActivity
        implements NavigationView.OnNavigationItemSelectedListener {
    MapView mapView=null;
    ArrayList<Marker> markerList=new ArrayList<>();
    AMap aMap=null;
    final static ArrayList<MsgInfo> msgInfos=new ArrayList<>();
    AMapLocationListener mLocationListener=null;
    public AMapLocationClient mLocationClient = null;
    public AMapLocationClientOption mLocationOption  = new AMapLocationClientOption();
    public  static final int RequestForLogin_Code=10;
    public OnLoaded onLoaded=null;
    public static boolean isLoading=false;

    @RequiresApi(api = Build.VERSION_CODES.M)
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        checkPermissions();
        getLocation();
        initMap(savedInstanceState);
        final ArrayList<Msg> msgList=new ArrayList<>();
        onLoaded=new OnLoaded(msgList,aMap,this,markerList);
        aMap.setOnMapLoadedListener(onLoaded);
        initLocation();


        //用来检查有没有被@,后端调试通再打开,千万不能删!!!!!!
//        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O) {
//            startForegroundService(new Intent(MainActivity.this, ShowNoticeService.class));
//        } else {
//            startService(new Intent(MainActivity.this, ShowNoticeService.class));
//        }
       // startService(new Intent(MainActivity.this,ShowNoticeService.class));


        Toolbar toolbar = (Toolbar) findViewById(R.id.toolbar);
        setSupportActionBar(toolbar);
        Button sendMsgBtn=findViewById(R.id.send_msg);
        findViewById(R.id.fresh).setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                //刷新信息
                if(!isLoading){
                    isLoading=true;
                    aMap.clear();
                    onLoaded.getMsgs();
                }

//                ArrayList<MsgInfo> msgInfos=new ArrayList<>();
//                msgInfos.add(new MsgInfo());
                //freshMsg(MainActivity.this,aMap,msgInfos);
            }
        });
        sendMsgBtn.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
               enterOrLogin(SendMsgActivity.class);

            }
        });
        //初始化地图

        aMap.setInfoWindowAdapter(new InfoWindow(this));//设置infowindow


        AMap.OnMarkerClickListener markerClickListener = new AMap.OnMarkerClickListener() {
            @Override
            public boolean onMarkerClick(Marker marker) {
                Intent intent=new Intent(MainActivity.this,DetailActivity.class);
                MsgInfo msgInfo= (MsgInfo) marker.getObject();
                intent.putExtra("msgId",msgInfo.msgId);
                intent.putExtra("imgUrls",msgInfo.imgUrls);
                startActivity(intent);
                return true;
            }
        };
        aMap.setOnMarkerClickListener(markerClickListener);
        //有bug,以后再修复
        AMap.OnMapLongClickListener longClickListener=new AMap.OnMapLongClickListener() {
            @Override
            public void onMapLongClick(LatLng latLng) {
                aMap.animateCamera(CameraUpdateFactory.changeLatLng(latLng));
                aMap.clear();
                for(Msg m:msgList) m.freshContent();
                for(Msg m:msgList){
                    markerList.add(aMap.addMarker(m.getMarkerOption()));
                }
                Marker marker=getMarkerInThisLatlng(latLng);
                if(marker!=null){
                    if(marker.isInfoWindowShown())
                        marker.hideInfoWindow();
                    else marker.showInfoWindow();
                }
            }
        };
        aMap.setOnMapLongClickListener(longClickListener);

        DrawerLayout drawer = (DrawerLayout) findViewById(R.id.drawer_layout);
        ActionBarDrawerToggle toggle = new ActionBarDrawerToggle(
                this, drawer, toolbar, R.string.navigation_drawer_open, R.string.navigation_drawer_close);
        drawer.addDrawerListener(toggle);
        toggle.syncState();

        NavigationView navigationView = (NavigationView) findViewById(R.id.nav_view);
        navigationView.setNavigationItemSelectedListener(this);
        View headerView=navigationView.getHeaderView(0);
        TextView textView=headerView.findViewById(R.id.login_tv);
        if(UserInfomation.isLogin(this)){//已登录
            textView.setText("赵日天");
        }
        else {
            textView.setOnClickListener(new View.OnClickListener() {
                @Override
                public void onClick(View v) {
                    startActivityForResult(new Intent(MainActivity.this,LoginActivity.class),RequestForLogin_Code);
                }
            });
        }
    }

    private void initLocation() {
        mLocationListener=new AMapLocationListener() {
            @Override
            public void onLocationChanged(AMapLocation aMapLocation) {
                if (aMapLocation != null) {
                    if (aMapLocation.getErrorCode() == 0) {
                        SharedPreferences shared=getSharedPreferences("share",MODE_PRIVATE);
                        SharedPreferences.Editor editor=shared.edit();
                        editor.putString("x",aMapLocation.getLatitude()+"");
                        editor.putString("y",aMapLocation.getLongitude()+"");
                        editor.putString("isLocation","1");
                        editor.commit();
                    }else {
                    }

                }
            }
        };
        mLocationClient = new AMapLocationClient(getApplicationContext());
        mLocationClient.setLocationListener(mLocationListener);
        mLocationOption.setLocationMode(AMapLocationClientOption.AMapLocationMode.Battery_Saving);
        mLocationOption.setOnceLocationLatest(true);
        mLocationClient.setLocationOption(mLocationOption);
        mLocationClient.startLocation();

    }

    private void getLocation() {
        AMapLocationClient mLocationClient = null;
        mLocationClient = new AMapLocationClient(getApplicationContext());
        mLocationClient.setLocationListener(mLocationListener);
        mLocationClient.startLocation();

    }

    //初始化地图
    public void initMap(Bundle savedInstanceState) {
        mapView=(MapView)findViewById(R.id.map);
        mapView.onCreate(savedInstanceState);
        aMap=mapView.getMap();
        UiSettings uiSettings = aMap.getUiSettings();
        uiSettings.setZoomControlsEnabled(false);//隐藏缩放控件
    }

    //安卓6以上的动态权限申请
    @RequiresApi(api = Build.VERSION_CODES.M)
    private void checkPermissions() {
        if (checkSelfPermission(Manifest.permission.WRITE_EXTERNAL_STORAGE) == PackageManager.PERMISSION_GRANTED
                && checkSelfPermission(Manifest.permission.CAMERA) == PackageManager.PERMISSION_GRANTED
                ) {
        } else {
            requestPermissions(new String[]{Manifest.permission.WRITE_EXTERNAL_STORAGE,
                    Manifest.permission.INTERNET,
                    Manifest.permission.CAMERA,
            Manifest.permission.ACCESS_NOTIFICATION_POLICY,
            Manifest.permission.ACCESS_FINE_LOCATION,
                    Manifest.permission.ACCESS_COARSE_LOCATION}, 100);
        }

    }

    @Override
    public void onBackPressed() {
        DrawerLayout drawer = (DrawerLayout) findViewById(R.id.drawer_layout);
        if (drawer.isDrawerOpen(GravityCompat.START)) {
            drawer.closeDrawer(GravityCompat.START);
        } else {
            super.onBackPressed();
        }
    }

    @Override
    public boolean onCreateOptionsMenu(Menu menu) {
        // Inflate the menu; this adds items to the action bar if it is present.
        getMenuInflater().inflate(R.menu.main, menu);
        return true;
    }

    @Override
    public boolean onOptionsItemSelected(MenuItem item) {
        // Handle action bar item clicks here. The action bar will
        // automatically handle clicks on the Home/Up button, so long
        // as you specify a parent activity in AndroidManifest.xml.
        int id = item.getItemId();

        //noinspection SimplifiableIfStatement
        if (id == R.id.action_settings) {
            return true;
        }

        return super.onOptionsItemSelected(item);
    }

    @RequiresApi(api = Build.VERSION_CODES.O)
    @SuppressWarnings("StatementWithEmptyBody")
    @Override
    public boolean onNavigationItemSelected(MenuItem item) {
        // Handle navigation view item clicks here.
        int id = item.getItemId();

         if (id == R.id.nav_gallery) {
             enterOrLogin(PersonalHomePageActivity.class);

        }  else if (id == R.id.nav_manage) {
             startActivity(new Intent(MainActivity.this,SettingActivity.class));
        } else if (id == R.id.nav_share) {
             ClipboardManager clip = (ClipboardManager)getSystemService(Context.CLIPBOARD_SERVICE);
             String shareMsg="我正在使用[顺呼--社交2.0],点击下载:http://lowee.top/WhistleWind/shunhu.apk 记得 QQ/微信 打开后在右上角选择用浏览器打开哦";
             clip.setText(shareMsg);
             Toast.makeText(this,"已在剪切板中,快去复制分享给你的小伙伴吧~",Toast.LENGTH_SHORT).show();
        }
        else if(id==R.id.nav_my_friend){
             enterOrLogin(FriendListActivity.class);
         }
         else if(id==R.id.nav_bug){
             startActivity(new Intent(this,BugreporterActivity.class));
         }
        DrawerLayout drawer = (DrawerLayout) findViewById(R.id.drawer_layout);
        drawer.closeDrawer(GravityCompat.START);
        return true;
    }

    public void enterOrLogin(Class activity){
        SharedPreferences shared=getSharedPreferences("share",MODE_PRIVATE);
        String userId=shared.getString("userId","");
        if(userId.equals("")){//没有登录
            startActivityForResult(new Intent(MainActivity.this,LoginActivity.class),RequestForLogin_Code);
        }
        else {
            Intent intent=new Intent(MainActivity.this,activity);
            intent.putExtra("userId",userId);
            startActivityForResult(intent,SendMsgActivity.From_Main_Activity);
        }
    }

    public LatLng[] getMapCenterPoint() {
        int left = mapView.getLeft();
        int top = mapView.getTop();
        int right = mapView.getRight();
        int bottom = mapView.getBottom();
        // 获得屏幕点击的位置
        int x = (int) (mapView.getX() + (right - left) / 2);
        int y = (int) (mapView.getY() + (bottom - top) / 2);
        Projection projection = aMap.getProjection();
        LatLng pt = projection.fromScreenLocation(new Point(x, y));
        LatLng[] latLngs=new LatLng[3];
        latLngs[0]=pt;//中心点
        latLngs[1]=projection.fromScreenLocation(new Point(((int)mapView.getX()+right),y));//右边
        latLngs[2]=projection.fromScreenLocation(new Point(x,((int)mapView.getY()+bottom)));//上边
        return latLngs;
    }



    @Override
    protected void onActivityResult(int requestCode, int resultCode, @Nullable Intent data) {
        if(resultCode==LoginActivity.Result_Code_Successful){
            super.onActivityResult(requestCode, resultCode, data);
            NavigationView navigationView = (NavigationView) findViewById(R.id.nav_view);
            navigationView.setNavigationItemSelectedListener(this);
            View headerView=navigationView.getHeaderView(0);
            TextView textView=headerView.findViewById(R.id.login_tv);
            textView.setText("赵日天");
        }
        else if(resultCode==SendMsgActivity.Send_Msg_Code){
            this.onLoaded.getMsgs();
        }


    }

    Marker getMarkerInThisLatlng(LatLng latLng){
        for(Marker marker:markerList){
            if(isInMarker(marker.getPosition(),latLng))
                return marker;
        }
        return null;
    }


    boolean isInMarker(LatLng markerLatLng,LatLng latLng){
        Point markerPos=aMap.getProjection().toScreenLocation(markerLatLng);
        Point clickPos=aMap.getProjection().toScreenLocation(latLng);
        if((clickPos.x>markerPos.x-200)&&(clickPos.x<markerPos.x+200)&&(clickPos.y>markerPos.y)&&(clickPos.y<markerPos.y+200))
            return true;
        else return false;
        }
        public static void freshMsg(Activity activity,AMap aMap,ArrayList<MsgInfo> msgInfos){
            Thread t=new Thread(new Runnable() {
                @Override
                public void run() {
                    ArrayList<Bitmap> bitmaps=new ArrayList<>();
                    for(MsgInfo msgInfo:msgInfos){
                        msgInfo.bitmap=InternetConnector.getBitmapFromUrl(msgInfo.imgUrl);
                    }
                    activity.runOnUiThread(new Runnable() {
                        @Override
                        public void run() {
                            Msg m=new Msg(activity,aMap,msgInfos.get(0));
                            aMap.addMarker(m.getMarkerOption());
                        }
                    });
                }
            });
            t.start();
        }
    class OnLoaded implements AMap.OnMapLoadedListener,Runnable, Callback {
        ArrayList<Msg> msgList=null;
        AMap aMap=null;
        Activity c=null;

        ArrayList<Marker> markerList=null;
        Bitmap bitmap=null;
        public OnLoaded(ArrayList<Msg> msgList, AMap aMap, Activity c, ArrayList<Marker> markerList){
            this.aMap=aMap;this.c=c;this.markerList=markerList;this.msgList=msgList;
        }
        public  void loadImg(){
            for(MsgInfo msgInfo: MainActivity.msgInfos){
                //msgInfo.bitmap=InternetConnector.getBitmapFromUrl(msgInfo.imgUrl);
                if(msgInfo.imgUrls.size()>0)
                    msgInfo.bitmap=InternetConnector.getBitmapFromUrl(InternetConnector.Img_Head+msgInfo.imgUrls.get(0));
                //msgInfo.bitmap=InternetConnector.getBitmapFromUrl(msgInfo.imgUrl);
                c.runOnUiThread(new Runnable() {
                    @Override
                    public void run() {
                        freshImg(msgInfo);
                    }
                });
            }
        }
        @Override
        public void onMapLoaded() {
            Thread t=new Thread(this);
            t.start();

        }

        public void freshImg(MsgInfo msgInfo){
            Msg m=new Msg(c,aMap,msgInfo);
            msgList.add(m);
            Marker marker=aMap.addMarker(m.getMarkerOption());
            marker.setObject(msgInfo);
            markerList.add(marker);
            isLoading=false;
//        for(int i=0;i<10;i++){
//            double x=0.1*i*Math.random();
//            double y=0.1*i*Math.random();
//            Msg m=new Msg(c,new LatLng(39.906901+x,116.397972+y),aMap,bitmap);
//            msgList.add(m);
//        }
//        for(Msg m:msgList){
//            markerList.add(aMap.addMarker(m.getMarkerOption()));
//        }
        }

        @Override
        public void run() {
            isLoading=true;
            getMsgs();
        }

        public void  getMsgs() {
            OkHttpClient okHttpClient=new OkHttpClient();
            HashMap<String,String> args=new HashMap<>();
//            args.put("x","0");
//            args.put("y","0");
//            args.put("zoom","0");
//            args.put("width","100");
//            args.put("height","100");
            args.put("zoom",String.valueOf(aMap.getCameraPosition().zoom));
            LatLng[] latLngs=getMapCenterPoint();
            args.put("x",String.valueOf(latLngs[0].latitude));
            args.put("y",String.valueOf(latLngs[0].longitude));
            args.put("width",String.valueOf(Math.abs(latLngs[0].latitude-latLngs[2].latitude)));
            args.put("height",String.valueOf(Math.abs(latLngs[0].longitude-latLngs[1].longitude)));
            //args.put("userId",UserInfomation.getUserId(c));
            Call call=okHttpClient.newCall(InternetConnector.getRequestForNewMsg(args));
            call.enqueue(this);
        }

        @Override
        public void onFailure(Call call, IOException e) {
            e.printStackTrace();
            showToast("你的网络状况貌似不太好哦,请稍后再试");
        }

        @Override
        public void onResponse(Call call, Response response) throws IOException {
            try {
                String res=response.body().string();

                //JSONObject json=new JSONObject(res);
                JSONArray jsonArray=new JSONArray(res);
                for(int i=0;i<jsonArray.length();i++){
                    JSONObject jsonObject=jsonArray.getJSONObject(i);
                    MsgInfo msgInfo=new MsgInfo();
                    msgInfo.content=jsonObject.getString("content");
                    msgInfo.title=jsonObject.getString("title");
                    String  urls_str=jsonObject.getString("img");
                    JSONArray urls=new JSONArray(urls_str);
                    for(int j=0;j<urls.length();j++){
                        msgInfo.imgUrls.add(urls.getString(j));
                    }
                    msgInfo.msgId=jsonObject.getString("msgId");
                    msgInfo.latLng=new LatLng(Double.valueOf(jsonObject.getString("x")),Double.valueOf(jsonObject.getString("y")));
                    msgInfo.c=c;
                    try{
                        if(msgInfo.title.equals("Title")){
                            msgInfo.title="距你"+String.valueOf(AMapUtils.calculateLineDistance(msgInfo.latLng,UserInfomation.getUserLatlng(msgInfo.c)))+"米";
                        }
                    }
                    catch (Exception e){
                        msgInfo.title="";
                    }


                    MainActivity.msgInfos.add(msgInfo);
                }
                loadImg();//下载图片


            } catch (JSONException e) {
                e.printStackTrace();
                showToast("哦No,出了点意外,刷新试试");
            }
        }

        private void  showToast(String msg){
            Looper.prepare();
            Toast.makeText(c,msg,Toast.LENGTH_SHORT).show();
            Looper.loop();
        }
    }
}
