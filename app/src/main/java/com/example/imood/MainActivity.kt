package com.example.imood

import android.os.Bundle
import androidx.appcompat.app.AppCompatActivity
import java.net.URL
import kotlin.io.readBytes

class MainActivity : AppCompatActivity() {
    //test
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.loginscreen)
        val apiResponse = URL("http://129.151.198.87:5000/iMood/getEmojis").readText()
        print(apiResponse)
    }
}