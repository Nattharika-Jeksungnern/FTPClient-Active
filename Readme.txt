1.อ้างอิงรูปแบบของ cmd window 11 โดยลองกับ server filezilla ซึ่งเป็นแบบ local เท่านั้น ไม่ได้ลองแบบ public
2.ติดตั้ง library เพิ่มเติม
    pip install maskpass  ใช้เมื่อ user ป้อน password แล้วซ่อนไว้
3.ในส่วนของ get และ ls ถ้าขนาดข้อมูลเป็น 0 จะไม่ขึ้นบรรทัด ftp: 22 bytes received in 0.00Seconds 22000.00Kbytes/sec. ในรูปแบบประมาณนี้ขึ้นมา
4.คำสั่งต้องพิมพ์ตัวเล็กเท่านั้น
5.การป้อน cmd และ input ทำได้หลายแบบเหมือนกับใน cmd
    Ex: get
        Remote file
        Local file
        ------------
        get filename
6.ตอนที่ get remote file มาจะถูกเก็บไว้ใน folder data 
