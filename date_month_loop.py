# add or minus month from input date 
def monthdelta(date, delta):
	m, y = (date.month+delta) % 12, date.year + ((date.month)+delta-1) // 12
	if not m: m = 12
	d = min(date.day, [31,
		29 if y%4==0 and not y%400==0 else 28,31,30,31,30,31,31,30,31,30,31][m-1])
	return date.replace(day=d,month=m, year=y)

def insert_consumption_detail_HT(meter_id,consumer_no):
	current_date = datetime.date.today()
	start_date = current_date - timedelta(days=365)

	if meter_id==None:
		PowerConsumerHTTotalService.objects.filter(consumer_no=consumer_no).update(m_id_crawl=1)
	else:
		
		while start_date<=current_date:
				month=start_date.month
				year=start_date.year
				count=PowerConsumerBillHTTotalService.objects.filter(consumer_no=consumer_no,bill_month=month,bill_year=year).count()
				if count==0:
					bill_month=start_date.strftime('%^b')+"-"+str(year)

					bill_data=monthly_consumption_data_HT(meter_id,bill_month)
					
					# count=PowerConsumerBillHTTotalService.objects.filter(consumer_no=consumer_no,	bill_month=month,bill_year=year).count()
					# if count==0:
					pcd=PowerConsumerBillHTTotalService(bill_month=month,bill_year=year,consumer_no=consumer_no,bill_kvah=bill_data['bill_kvah'],bill_kwh=bill_data['bill_kwh'])
					pcd.save()
					
				date =monthdelta(start_date,1)
				start_date=datetime.date(date.year,date.month,date.day)

		PowerConsumerHTTotalService.objects.filter(consumer_no=consumer_no).update(m_id_crawl=1)
	return 1