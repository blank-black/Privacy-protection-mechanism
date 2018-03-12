package com.example.admin.myapplication;

import android.app.DownloadManager;
import android.content.Intent;
import android.content.SharedPreferences;
import android.os.Build;
import android.os.Bundle;
import android.support.v7.app.AlertDialog;
import android.support.v7.app.AppCompatActivity;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.CheckBox;
import android.widget.EditText;
import android.widget.Toast;

import com.android.volley.AuthFailureError;
import com.android.volley.RequestQueue;
import com.android.volley.Request;
import com.android.volley.Response;
import com.android.volley.VolleyError;
import com.android.volley.toolbox.StringRequest;
import com.android.volley.toolbox.Volley;

import org.json.JSONObject;

import java.util.HashMap;
import java.util.Map;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

public class LoginActivity extends AppCompatActivity {
    private EditText mAccount;                        //用户名编辑
    private EditText mPwd;                            //密码编辑
    private Button mRegisterButton;                   //注册按钮
    private Button mLoginButton;                      //登录按钮
    private CheckBox mRememberCheck;
    private SharedPreferences login_sp;
    String res;
    boolean err;
    private static Toast toast;

    @Override
    public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_login);
        mAccount = (EditText) findViewById(R.id.login_edit_account);
        mPwd = (EditText) findViewById(R.id.login_edit_pwd);
        mRegisterButton = (Button) findViewById(R.id.login_btn_register);
        mLoginButton = (Button) findViewById((R.id.login_btn_login));
        mRememberCheck = (CheckBox) findViewById(R.id.Login_Remember);

        login_sp = getSharedPreferences("userInfo", 0);
        String name = login_sp.getString("USER_NAME", "");
        String pwd = login_sp.getString("PASSWORD", "");
        boolean choseRemember = login_sp.getBoolean("mRememberCheck", false);
        if (choseRemember) {
            mAccount.setText(name);
            mPwd.setText(pwd);
            mRememberCheck.setChecked(true);
        }


        View.OnClickListener mListener = new View.OnClickListener() {                  //不同按钮按下的监听事件选择
            public void onClick(View v) {
                switch (v.getId()) {
                    case R.id.login_btn_register:                            //登录界面的注册按钮
                        Intent intent_Login_to_Register = new Intent(LoginActivity.this, Register.class);    //切换Login Activity至User Activity
                        startActivity(intent_Login_to_Register);
                        finish();
                        break;
                    case R.id.login_btn_login:                              //登录界面的登录按钮
                        login_main();
                        break;

                }
            }
        };
        mRegisterButton.setOnClickListener(mListener);                      //采用OnClickListener方法设置不同按钮按下之后的监听事件
        mLoginButton.setOnClickListener(mListener);
    }

    public void login_main() {
        /*登录函数
        * */
        StringRequest login_item = login(mAccount.getText().toString(), mPwd.getText().toString());

        RequestQueue queue = Volley.newRequestQueue(this);
        queue.add(login_item);


      /*  String pattern = "\"status\":\"(\\d)\":\"count\":(\\d+)\"";
        Pattern r = Pattern.compile(pattern);
        Matcher m = r.matcher(res);
        if (Integer.parseInt(m.group(0))  == 0){
            Intent intent_Login_to_Register = new Intent(LoginActivity.this, Main_Activity.class);    //切换Login Activity至main Activity
            Bundle bundle = new Bundle();

            bundle.putString("username", mAccount.getText().toString());
            intent_Login_to_Register.putExtras(bundle);
            startActivity(intent_Login_to_Register);
            finish();
        }
        else{
            String content=String.format("账号密码输入错误\n 还可以尝试%s次", m.group(1));
            if (toast == null){
                toast=Toast.makeText(this, content , Toast.LENGTH_SHORT);
                toast.show();
            }else {
                toast.setText(content);
                toast.show();
            }




        }*/


    }

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

    public StringRequest login(String username, String password){
        final String uid = username;
        final String pw = password;
        final String model= getPesudoUniqueID();
        return new StringRequest(Request.Method.POST,"http://101.132.194.57:5000/username",
                new Response.Listener<String>(){
                    @Override
                    public void onResponse(String response) {
                        res=response;
                        Log.d("tag",res);
                        err = false;
                    }
                }, new Response.ErrorListener() {
            @Override
            public void onErrorResponse(VolleyError error) {
                Log.e("Err","That didn't work! " + error.getMessage());
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
                map.put( "count","1");
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


}

