#g~~fwlist~~ 2 w~~hat~~ online ~~generator~~
##在线生成gfwlist相关文件

##pac
`https://g2w.online` + `/pac/` + `类型首字母 逗号 IP 冒号 端口`
                     
举例，最常见类型`socks`，地址`192.168.1.1:1080`：                     
[https://g2w.online/pac/s,192.168.1.1:1080](https://g2w.online/pac/s,192.168.1.1:1080)               


包含`SOCKS5`和`SOCKS`两条参数，safari可以正常使用。
        
http类型把`s`改成`h`即可。
          
可以用加号组合（最多10个）：            
[https://g2w.online/pac/s,192.168.1.1:1080+h,127.0.0.1:1080](https://g2w.online/pac/s,192.168.1.1:1080+h,127.0.0.1:1080)     

## dnsmasq + ipset
`https://g2w.online` + `/ipset/` + `ipset名称 逗号 IP 冒号 端口`          
举例，`gfwipset`和`127.0.0.1:1053`：            
[https://g2w.online/ipset/gfwipset,127.0.0.1:1053](https://g2w.online/ipset/gfwipset,127.0.0.1:1053)             
**名称限制下划线、数字、大小写字母，长度20以内。**

## 单 dnsmasq
`https://g2w.online/` + `/dnsq/` + ` IP 冒号 端口`               
举例，`127.0.0.1:1053`：            
[https://g2w.online/dnsq/127.0.0.1:1053](https://g2w.online/ipset/127.0.0.1:1053)        
## 其它
等待添加