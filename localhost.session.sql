SELECT devices.device_name, (SELECT MAX(data_date) FROM devicedatas 
WHERE data_id = d.data_id
) ,
 d.temperature, d.humidity
  FROM devicedatas d INNER JOIN devices ON devices.device_id = d.device_id 
WHERE devices.device_name IS NOT NULL