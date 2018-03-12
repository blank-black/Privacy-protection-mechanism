package com.wk_1552157.test;

import android.Manifest;
import android.content.pm.PackageManager;
import android.graphics.Bitmap;
import android.os.Build;
import android.support.v4.content.ContextCompat;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.view.View;
import android.view.View.OnClickListener;
import android.widget.ImageView;
import android.widget.TextView;
import android.util.Log;
import android.telephony.TelephonyManager;

import com.android.volley.AuthFailureError;
import com.android.volley.Request;
import com.android.volley.RequestQueue;
import com.android.volley.Response;
import com.android.volley.VolleyError;
import com.android.volley.toolbox.ImageLoader;
import com.android.volley.toolbox.StringRequest;
import com.android.volley.toolbox.Volley;

import java.util.HashMap;
import java.util.Map;

public class MainActivity extends AppCompatActivity implements OnClickListener{
    String res;
    boolean err;
    public String getPesudoUniqueID() {
        String m_szDevIDShort = "35" + //we make this look like a valid IMEI
                Build.BOARD.length() % 10 +
                Build.BRAND.length() % 10 +
                Build.DEVICE.length() % 10 +
                Build.DISPLAY.length() % 10 +
                Build.HOST.length() % 10 +
                Build.ID.length() % 10 +
                Build.MANUFACTURER.length() % 10 +
                Build.MODEL.length() % 10 +
                Build.PRODUCT.length() % 10 +
                Build.TAGS.length() % 10 +
                Build.TYPE.length() % 10 +
                Build.USER.length() % 10; //13 digits
        return m_szDevIDShort;
    }
    public String getIMEI() {
        String szImei;
        TelephonyManager TelephonyMgr = (TelephonyManager) MainActivity.this.getApplicationContext().getSystemService(TELEPHONY_SERVICE);
        if(ContextCompat.checkSelfPermission(this,android.Manifest.permission.ACCESS_FINE_LOCATION)== PackageManager.PERMISSION_GRANTED) {
            szImei = TelephonyMgr.getDeviceId();
            return szImei;
        }
        return null;
    }
    public StringRequest login(String username, String password){
        final String uid = username;
        final String pw = password;
        final String model= getPesudoUniqueID();
        return new StringRequest(Request.Method.POST,"http://101.132.194.57:5000/username",
                new Response.Listener<String>(){
                    @Override
                    public void onResponse(String response) {
                        res=response;
                        err = false;
                    }
                }, new Response.ErrorListener() {
            @Override
            public void onErrorResponse(VolleyError error) {
                res=error.getMessage();
                err = true;
            }
        }){
            @Override
            protected Map<String,String> getParams() throws AuthFailureError{
                Map<String,String> map = new HashMap<>();
                map.put("action","login");
                map.put("username",uid);
                map.put("password",pw);
                map.put("tools",model);
                return map;
            }
        };
    }
    public StringRequest getUserInfo(String username){
        final String uid = username;
        return new StringRequest(Request.Method.POST,"http://101.132.194.57:5000/username",
                new Response.Listener<String>(){
                    @Override
                    public void onResponse(String response) {
                        res=response;
                        err = false;
                    }
                }, new Response.ErrorListener() {
            @Override
            public void onErrorResponse(VolleyError error) {
                res=error.getMessage();
                err = true;
            }
        }){
            @Override
            protected Map<String,String> getParams() throws AuthFailureError{
                Map<String,String> map = new HashMap<>();
                map.put("action","getinfo");
                map.put("username",uid);
                return map;
            }
        };
    }
    public StringRequest getMicroBloc(String username){
        final String uid = username;
        return new StringRequest(Request.Method.POST,"http://101.132.194.57:5000/username",
                new Response.Listener<String>(){
                    @Override
                    public void onResponse(String response) {
                        res=response;
                        err = false;
                    }
                }, new Response.ErrorListener() {
                    @Override
                    public void onErrorResponse(VolleyError error) {
                        res=error.getMessage();
                        err = true;
                    }
        }){
            @Override
            protected Map<String,String> getParams() throws AuthFailureError{
                Map<String,String> map = new HashMap<>();
                map.put("action","getbloc");
                map.put("username",uid);
                return map;
            }
        };
    }
    public void showImg(ImageView img, String url, RequestQueue queue){
        ImageLoader imgloader = new ImageLoader(queue, new ImageLoader.ImageCache(){
            @Override
            public void putBitmap(String url, Bitmap bitmap) {
            }
            @Override
            public Bitmap getBitmap(String url) {
                return null;
            }
        });
        ImageLoader.ImageListener imglistener = ImageLoader.getImageListener(img,
                R.mipmap.loading, R.mipmap.ic_launcher);
        imgloader.get(url, imglistener);
    }
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        findViewById(R.id.button).setOnClickListener(MainActivity.this);
    }
    @Override
    public void onClick(View v){
        if(v.getId()==R.id.button){
            final TextView tv;
            tv=findViewById(R.id.textView);

            String   model= getPesudoUniqueID();
            Log.d("Tag","Response is: "+ model);
            tv.setText(model);
            // Instantiate the RequestQueue.
            //RequestQueue queue = Volley.newRequestQueue(this);
            //StringRequest request = getMicroBloc("2139359753");
            // Add the request to the RequestQueue.
            //queue.add(request);
        }
    }
}
