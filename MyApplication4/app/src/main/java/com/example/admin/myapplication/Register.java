package com.example.admin.myapplication;

import android.content.Intent;
import android.os.Bundle;
import android.support.v7.app.AppCompatActivity;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;

/**
 * Created by admin on 2018/3/6.
 */

public class Register extends AppCompatActivity {
    private EditText mAccount;                        //用户名编辑
    private EditText mPwd;                            //密码编辑
    private EditText mPwdCheck;                       //密码编辑
    private Button mSureButton;                       //确定按钮
    private Button mCancelButton;                     //取消按钮
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_register);
        mAccount = (EditText) findViewById(R.id.resetpwd_edit_name);
        mPwd = (EditText) findViewById(R.id.resetpwd_edit_pwd_old);
        mPwdCheck = (EditText) findViewById(R.id.resetpwd_edit_pwd_new);

        mSureButton = (Button) findViewById(R.id.register_btn_sure);
        mCancelButton = (Button) findViewById(R.id.register_btn_cancel);
        View.OnClickListener m_register_Listener = new View.OnClickListener() {    //不同按钮按下的监听事件选择
            public void onClick(View v) {
                switch (v.getId()) {
                    case R.id.register_btn_sure:                       //确认按钮的监听事件
                        register_check();
                        break;
                    case R.id.register_btn_cancel:                     //取消按钮的监听事件,由注册界面返回登录界面
                        Intent intent_Register_to_Login = new Intent(Register.this,LoginActivity.class) ;    //切换User Activity至Login Activity
                        startActivity(intent_Register_to_Login);
                        finish();
                        break;
                }
            }
        };

        mSureButton.setOnClickListener(m_register_Listener);      //注册界面两个按钮的监听事件
        mCancelButton.setOnClickListener(m_register_Listener);
    }
    public void register_check(){
        /*注册函数*/
        Intent intent_Register_to_Login = new Intent(Register.this,LoginActivity.class) ;    //切换User Activity至Login Activity
        startActivity(intent_Register_to_Login);
        finish();
    }

}
