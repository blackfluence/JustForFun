package test.liuxin.network;

import java.io.IOException;
import java.io.InputStream;
import java.net.URL;
import java.util.Date;
import java.util.concurrent.Callable;
import java.util.concurrent.ExecutionException;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import java.util.concurrent.Future;
import java.util.concurrent.TimeUnit;
import java.util.concurrent.TimeoutException;

/**
 * 
 * @author liuxin
 *
 */
public class CheckOnline2 {
	static Future future = null;
	static ExecutorService es = null;
	static Callable<String> callable = null;

	public static void main(String[] args) {
		es = Executors.newFixedThreadPool(1);
		callable = new Callable<String>() {			// 使用Callable接口作为构造参数
			@Override
			public String call() throws Exception {// 真正的任务在这里执行，这里的返回值类型为String，可以为任意类型
				URL url = new URL("http://baidu.com");
				InputStream in = url.openStream();
				in.close();
				return "0";
			}
		};
		netListen();
			
	}
	public static void reConnect(){
		Thread thread = new Thread();
		Process p = null;
		System.out.println(new Date().toLocaleString()+" 正在开始重连...");
		
		while(!checkOnline())
		{
			try {
				Runtime.getRuntime().exec("taskkill /F /IM srun3000.exe");
				thread.sleep(500);
				Runtime rn = Runtime.getRuntime();
				try {
					System.out.println(new Date().toLocaleString()+" 正在重启深澜客户端");
					p = rn.exec("\"srun3000.exe\"");
				} catch (Exception e) {
					System.out.println("Error exec!");
				}
				thread.sleep(5000);
			} catch (InterruptedException | IOException e) {
				e.printStackTrace();
			}
		}
		netListen();
	}
	public static void netListen()
	{
		Thread thread = new Thread();
		if(checkOnline())
			System.out.println(new Date().toLocaleString()+" 网络连接正常，监听中...");
		try {
			thread.sleep(1000);
		} catch (InterruptedException e) {
			e.printStackTrace();
		}
		while(checkOnline())
		{
			try {
				thread.sleep(1000);
			} catch (InterruptedException e) {
				e.printStackTrace();
			}
		}
		System.out.println(new Date().toLocaleString()+" 网络断开");
		reConnect();
	}
	public static boolean checkOnline() {
		try {
			future = es.submit(callable);
			String value = null;
			try {
				future.get(1000, TimeUnit.MILLISECONDS).toString();// 取得结果，同时设置超时执行时间为1秒。
				return true;
			} catch (ExecutionException | TimeoutException e) {
				return false;
			}
		} catch (InterruptedException e) {
			return false;
		}
	}
}
