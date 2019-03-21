package com.example.pc.sj;

import android.app.Notification;
import android.app.NotificationChannel;
import android.app.NotificationManager;
import android.app.PendingIntent;
import android.app.Service;
import android.content.Context;
import android.content.Intent;
import android.os.Build;
import android.os.IBinder;
import android.os.Looper;
import android.support.annotation.RequiresApi;
import android.widget.Toast;

import org.json.JSONException;
import org.json.JSONObject;

import java.io.IOException;

import okhttp3.Call;
import okhttp3.Callback;
import okhttp3.OkHttpClient;
import okhttp3.Response;

public class ShowNoticeService extends Service implements Callback {
    int i=0;
    Thread quaryNotice=null;//每隔一段时间查询是否有需要通知的消息
    OkHttpClient okHttpClient=new OkHttpClient();

    @Override
    public void onCreate() {
        super.onCreate();
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O) {
            //这个id不要和应用内的其他同志id一样，不行就写 int.maxValue()        //context.startForeground(SERVICE_ID, builder.getNotification());
        }
    }

    @Override
    public int onStartCommand(Intent intent, int flags, int startId) {
        new Thread(){
            @RequiresApi(api = Build.VERSION_CODES.O)
            @Override
            public void run() {
                int i=0;
                //循环申请,查询是否有需要通知的信息,目前设计一分钟检查一次
//                while (true){
//                    try {
//                        Thread.sleep(1000*60);
//                    } catch (InterruptedException e) {
//                        e.printStackTrace();
//                    }
                    quaryNotice();
//                }

            }
        }.start();
        return super.onStartCommand(intent, flags, startId);
    }

    @Override
    public IBinder onBind(Intent intent) {
        return null;
    }




    public void show(int i,String title,String content,String msgId){
        Intent intent=new Intent(ShowNoticeService.this,DetailActivity.class);
        intent.putExtra("title",title);
        intent.putExtra("content",content);
        intent.putExtra("msgId",msgId);
        intent.putExtra("imgUrl","http://i2.hdslb.com/bfs/archive/df77d8a9e3199df917cb6a68ffff2890059821d6.jpg");
        PendingIntent pendingIntent=PendingIntent.getActivity(this,0,intent,PendingIntent.FLAG_CANCEL_CURRENT);

        NotificationManager notifyManager = (NotificationManager) getSystemService(Context.NOTIFICATION_SERVICE);
        if (android.os.Build.VERSION.SDK_INT >= android.os.Build.VERSION_CODES.O){
            //适配安卓8以上
            NotificationChannel mChannel = new NotificationChannel(""+i, "name", NotificationManager.IMPORTANCE_LOW);
            notifyManager.createNotificationChannel(mChannel);
            Notification.Builder builder = new Notification.Builder(ShowNoticeService.this)
                    .setChannelId(""+i)
                    .setSmallIcon(R.mipmap.ic_launcher)
                    .setContentTitle(title)
                    .setContentText(content)
                    .setContentIntent(pendingIntent)
                    .setWhen(System.currentTimeMillis());
            Notification notification = builder.build();
            notifyManager.notify(i, notification);
        }
        else {
            Notification.Builder builder = new Notification.Builder(ShowNoticeService.this)
                    .setSmallIcon(R.mipmap.icon)
                    .setContentTitle("最简单的Notification")
                    .setContentText("只有小图标、标题、内容")
                    .setContentIntent(pendingIntent)
                    .setWhen(System.currentTimeMillis());
            Notification notification = builder.build();
            notifyManager.notify(i, notification);
        }


    }
    public void quaryNotice(){
        Call call=okHttpClient.newCall(InternetConnector.getRequestForNotice());
        call.enqueue(this);
    }

    @Override
    public void onFailure(Call call, IOException e) {
        Looper.prepare();
        Toast.makeText(this,"失败",Toast.LENGTH_SHORT).show();
        Looper.loop();
    }

    @Override
    public void onResponse(Call call, Response response) throws IOException {
        try {
            String json=response.body().string();
            JSONObject jsonObject=new JSONObject(json);
            String title=jsonObject.getString("title");
            String content=jsonObject.getString("content");
            String msgId=jsonObject.getString("msgId");
            show(i++,title,content,msgId);
        } catch (JSONException e) {
            e.printStackTrace();
        }
    }
}
