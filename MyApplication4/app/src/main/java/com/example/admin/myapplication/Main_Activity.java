package com.example.admin.myapplication;

import android.app.FragmentManager;
import android.app.FragmentTransaction;
import android.content.Intent;
import android.os.Build;
import android.os.Bundle;
import android.support.annotation.RequiresApi;
import android.support.v7.app.AppCompatActivity;
import android.util.Log;
import android.view.View;
import android.view.Window;
import android.widget.FrameLayout;
import android.widget.TextView;

import com.android.volley.AuthFailureError;
import com.android.volley.Request;
import com.android.volley.RequestQueue;
import com.android.volley.Response;
import com.android.volley.VolleyError;
import com.android.volley.toolbox.StringRequest;
import com.android.volley.toolbox.Volley;

import java.util.HashMap;
import java.util.Map;

/**
 * Created by admin on 2018/3/6.
 */

public class Main_Activity extends AppCompatActivity implements View.OnClickListener {
    private TextView topBar;
    private TextView tabDeal;
    private TextView tabPoi;

    private TextView tabUser;

    private FrameLayout ly_content;

    private FirstFragment f1,f2,f3,f4;
    private FragmentManager fragmentManager;
    String res_userinfo;
    String res_microblog;
    Boolean  err;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);

        setContentView(R.layout.activity_main);
        Intent intent=getIntent();

        String username=intent.getStringExtra("username");
        StringRequest Micro_item = getMicroBloc(username);
        StringRequest User_item = getUserInfo(username);

        RequestQueue queue = Volley.newRequestQueue(this);
        queue.add(Micro_item);
        queue.add(User_item);

        bindView();

    }
    private void bindView() {
        topBar = (TextView)this.findViewById(R.id.txt_top);
        tabDeal = (TextView)this.findViewById(R.id.txt_deal);
        tabPoi = (TextView)this.findViewById(R.id.txt_poi);
        tabUser = (TextView)this.findViewById(R.id.txt_user);

        ly_content = (FrameLayout) findViewById(R.id.fragment_container);

        tabDeal.setOnClickListener(this);

        tabUser.setOnClickListener(this);
        tabPoi.setOnClickListener(this);

    }
    public void selected(){
        tabDeal.setSelected(false);

        tabPoi.setSelected(false);
        tabUser.setSelected(false);
    }
    public void hideAllFragment(FragmentTransaction transaction){
        if(f1!=null){
            transaction.hide(f1);
        }
        if(f2!=null){
            transaction.hide(f2);
        }
        if(f3!=null){
            transaction.hide(f3);
        }
        if(f4!=null){
            transaction.hide(f4);
        }
    }
    @Override
    public void onClick(View v) {
        FragmentTransaction transaction = getFragmentManager().beginTransaction();
        hideAllFragment(transaction);
        switch(v.getId()){
            case R.id.txt_deal:
                selected();
                tabDeal.setSelected(true);
                if(f1==null){
                    f1 = new FirstFragment("用户之间的对话");
                    transaction.add(R.id.fragment_container,f1);
                }else{
                    transaction.show(f1);
                }
                break;


            case R.id.txt_poi:
                selected();
                tabPoi.setSelected(true);
                if(f3==null){
                    f3 = new FirstFragment(res_userinfo);
                    transaction.add(R.id.fragment_container,f3);
                }else{
                    transaction.show(f3);
                }
                break;

            case R.id.txt_user:
                selected();
                tabUser.setSelected(true);
                if(f4==null){
                    f4 = new FirstFragment(res_microblog);
                    transaction.add(R.id.fragment_container,f4);
                }else{
                    transaction.show(f4);
                }
                break;
        }

        transaction.commit();
    }
    public StringRequest getUserInfo(String username){
        final String uid = username;
        return new StringRequest(Request.Method.POST,"http://101.132.194.57:5000/username",
                new Response.Listener<String>(){
                    @Override
                    public void onResponse(String response) {
                        res_userinfo=response;
                        err = false;
                    }
                }, new Response.ErrorListener() {
            @Override
            public void onErrorResponse(VolleyError error) {
                res_userinfo=error.getMessage();
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
                        res_microblog=response;
                        err = false;
                    }
                }, new Response.ErrorListener() {
            @Override
            public void onErrorResponse(VolleyError error) {
                res_microblog=error.getMessage();
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

}
