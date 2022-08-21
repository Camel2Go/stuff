package com.ffxf.holoapp

import android.app.Activity
import android.content.Context
import android.content.Intent
import android.content.IntentFilter
import android.content.pm.ActivityInfo
import android.media.AudioManager
import android.net.Uri
import android.os.Build
import android.os.Bundle
import android.util.Log
import android.view.KeyEvent
import android.view.View
import android.view.WindowManager
import android.widget.VideoView
import androidx.annotation.RequiresApi
import java.io.File
import android.content.BroadcastReceiver


class VideoPlayerActivity : Activity(){
    private val TAG: String = VideoPlayerActivity::class.java.simpleName
    private lateinit var mVV: VideoView
    private lateinit var audioManager: AudioManager
    private var isInitialVolumeKeyPressed = true
    private val screenOffReceiver = object: BroadcastReceiver() {
        override fun onReceive(context: Context, intent: Intent) {
            mVV.stopPlayback()
            finish();
            val proc = Runtime.getRuntime().exec(arrayOf("su", "-c", "reboot -p"))
            proc.waitFor()
        }
    }

    @RequiresApi(Build.VERSION_CODES.R)
    override fun onCreate(savedInstanceState: Bundle?) {

        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_video_player)

        // create and register ScreenOffReceiver
        val filter = IntentFilter(Intent.ACTION_SCREEN_OFF)
        registerReceiver(screenOffReceiver, filter)

        // change orientation
        requestedOrientation = ActivityInfo.SCREEN_ORIENTATION_LANDSCAPE

        // hide navigation-bar
        // window.insetsController?.hide(WindowInsets.Type.navigationBars())
        window.decorView.apply { systemUiVisibility = View.SYSTEM_UI_FLAG_HIDE_NAVIGATION or View.SYSTEM_UI_FLAG_FULLSCREEN }

        // show on lockscreen
        window.addFlags(WindowManager.LayoutParams.FLAG_DISMISS_KEYGUARD)
        window.addFlags(WindowManager.LayoutParams.FLAG_SHOW_WHEN_LOCKED)
        window.addFlags(WindowManager.LayoutParams.FLAG_TURN_SCREEN_ON)
        window.addFlags(WindowManager.LayoutParams.FLAG_KEEP_SCREEN_ON)

        // get AudioManager
        audioManager = getSystemService(Context.AUDIO_SERVICE) as AudioManager

        // create VideoPlayer for given file
        val videoFile = this.intent.extras?.get("videoFile") as File
        mVV = findViewById<View>(R.id.videoview) as VideoView
        mVV.setOnPreparedListener { it.isLooping = true }
        mVV.setVideoURI(Uri.fromFile(videoFile))
        mVV.start()
    }

    override fun onKeyDown(keyCode: Int, event: KeyEvent): Boolean {

        if (keyCode == KeyEvent.KEYCODE_VOLUME_UP || keyCode == KeyEvent.KEYCODE_VOLUME_DOWN) {
            event.startTracking()
            return true
        }
        return super.onKeyDown(keyCode, event)
    }

    override fun onKeyUp(keyCode: Int, event: KeyEvent): Boolean {

        if (!isInitialVolumeKeyPressed and !event.isCanceled) {
            when (keyCode) {
                KeyEvent.KEYCODE_VOLUME_UP -> audioManager.adjustStreamVolume(
                    AudioManager.STREAM_MUSIC,
                    AudioManager.ADJUST_RAISE,
                    AudioManager.FLAG_SHOW_UI
                )
                KeyEvent.KEYCODE_VOLUME_DOWN -> audioManager.adjustStreamVolume(
                    AudioManager.STREAM_MUSIC,
                    AudioManager.ADJUST_LOWER,
                    AudioManager.FLAG_SHOW_UI
                )
            }
        }
        isInitialVolumeKeyPressed = false
        return super.onKeyUp(keyCode, event)
    }

    override fun onKeyLongPress(keyCode: Int, event: KeyEvent?): Boolean {
        if (keyCode == KeyEvent.KEYCODE_VOLUME_UP || keyCode == KeyEvent.KEYCODE_VOLUME_DOWN) {
            val keyCodeIntent = Intent()
            keyCodeIntent.putExtra("keyCode", keyCode)
            this.setResult(Activity.RESULT_OK, keyCodeIntent)
            this.finish()
            return true
        }
        return super.onKeyLongPress(keyCode, event)
    }

    override fun finish() {
        super.finish()
        unregisterReceiver(screenOffReceiver)
    }
}