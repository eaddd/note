@"%SystemRoot%\System32\WindowsPowerShell\v1.0\powershell.exe" -NoProfile -InputFormat None -ExecutionPolicy Bypass -Command "iex ((New-Object System.Net.WebClient).DownloadString('https://chocolatey.org/install.ps1'))" && SET "PATH=%PATH%;%ALLUSERSPROFILE%\chocolatey\bin"


E:\mongoDB\mongodb-4.0.4\bin\mongod.exe --config E:\mongoDB\mongodb-4.0.4\mongo.conf --serviceName "MongoDB" --serviceDisplayName "MongoDB" --install


db.createUser( 
{ 
    user: "admin", 
    pwd: "123456", 
    roles: [{ role: "userAdminAnyDatabase", db: "admin" }] 
})

db.createUser({user:'gaatdd',pwd:'123456',roles:[{role:'readWrite',db:'wx_sales'}]})


db.grantRolesToUser(
    "gaatdd",
    [
      { role: "userAdmin", db: "wx_sales" }
    ]
)


use wx_sales
db.createUser(
  {
    user: "gaatdd",
    pwd: "123456",
    roles: [ { role: "readWrite", db: "wx_sales" },
             { role: "read", db: "reporting" } ]
  }
)

mongo --host localhost -u "gaatdd" --authenticationDatabase "test" -p'123456' 