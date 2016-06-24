import wmi
import Def_Locale

def Calc_UTC_Min(min):
	temp = min%60
	if temp==0:
		return "00"
	else:
		return str(temp)

def Parse_Datetime(datetime):
	return datetime[0:4]+"/"+datetime[4:6]+"/"+datetime[6:8]+" "+datetime[8:10]+":"+datetime[10:12]+":"+datetime[12:]

def get_process_info(wmi_pointer):
	codepage=wmi_pointer.Win32_OperatingSystem(["CodeSet"])[0].CodeSet
	print "*System INFO"
	print "  -Windows Version\t:", wmi_pointer.Win32_OperatingSystem(["Caption"])[0].Caption
	print "  -Windows BuildNumber\t:", wmi_pointer.Win32_OperatingSystem(["BuildNumber"])[0].BuildNumber
	print "  -Windows Setup time\t:", Parse_Datetime(wmi_pointer.Win32_OperatingSystem(["InstallDate"])[0].InstallDate.split('+')[0]),
	print "(UTC +", int(wmi_pointer.Win32_OperatingSystem(["InstallDate"])[0].InstallDate.split('+')[1])/60, ":", 
	print Calc_UTC_Min(int(wmi_pointer.Win32_OperatingSystem(["InstallDate"])[0].InstallDate.split('+')[1])), ")"
	print "\n*System"
	print "  -Processor Name\t:", wmi_pointer.Win32_Processor(["Name"])[0].Name
	print "  -Processor ID \t:", wmi_pointer.Win32_Processor(["ProcessorID"])[0].ProcessorID
#	print "  -Processor Load Info\t:", wmi_pointer.Win32_Processor(["LoadPercentage"])[0].LoadPercentage
	print "  -Physical_Mem Size\t:", int(wmi_pointer.Win32_PhysicalMemory(["Capacity"])[0].Capacity)/1048576/1024, "GByte"
#	print "  -Vitual_Mem Size\t:", int(wmi_pointer.Win32_OperatingSystem(["TotalVirtualMemorySize"])[0].TotalVirtualMemorySize)/1048576, "Byte"
	print "  -System Type(84/64)\t:", wmi_pointer.Win32_OperatingSystem(["OSArchitecture"])[0].OSArchitecture
	print "  -Computer name\t:", wmi_pointer.Win32_OperatingSystem(["CSName"])[0].CSName
	print "\n*User"
	print "  -User count\t\t:",wmi_pointer.Win32_OperatingSystem(["NumberOfUsers"])[0].NumberOfUsers
	print "  -User name\t\t:",wmi_pointer.Win32_OperatingSystem(["RegisteredUser"])[0].RegisteredUser
	print "\n*Detail Info"
	print "  -CodePage\t\t:", codepage
	print "  -CountryCode\t\t:", wmi_pointer.Win32_OperatingSystem(["CountryCode"])[0].CountryCode
	print "  -Locale\t\t:", Def_Locale.List[hex(int(wmi_pointer.Win32_OperatingSystem(["Locale"])[0].Locale,16))[2:]]
	print "  -MUILanguage\t\t:", wmi_pointer.Win32_OperatingSystem(["MUILanguages"])[0].MUILanguages[0]
	print "  -UTC\t\t\t: +", wmi_pointer.Win32_OperatingSystem(["CurrentTimeZone"])[0].CurrentTimeZone/60,
	print ":", Calc_UTC_Min(int(wmi_pointer.Win32_OperatingSystem(["CurrentTimeZone"])[0].CurrentTimeZone))
	print "  -Serial Number\t:",wmi_pointer.Win32_OperatingSystem(["SerialNumber"])[0].SerialNumber 
	print "  -Last BootUP time\t:", Parse_Datetime(wmi_pointer.Win32_OperatingSystem(["LastBootUpTime"])[0].LastBootUpTime.split('+')[0]),
	print "(UTC +", int(wmi_pointer.Win32_OperatingSystem(["LastBootUpTime"])[0].LastBootUpTime.split('+')[1])/60, ":", 
	print Calc_UTC_Min(int(wmi_pointer.Win32_OperatingSystem(["LastBootUpTime"])[0].LastBootUpTime.split('+')[1])), ")"
	print "  -System Drive\t\t:",wmi_pointer.Win32_OperatingSystem(["SystemDrive"])[0].SystemDrive
	print "  -System Dircetory\t:",wmi_pointer.Win32_OperatingSystem(["SystemDirectory"])[0].SystemDirectory
	print "  -Boot Device\t\t:",wmi_pointer.Win32_OperatingSystem(["BootDevice"])[0].BootDevice
	print "  -Process Cnt\t\t:",wmi_pointer.Win32_OperatingSystem(["NumberOfProcesses"])[0].NumberOfProcesses
	print "\n*Storage"
	print "  -Number of Storgae\t:", len(wmi_pointer.Win32_DiskDrive(["Caption"]))
	print "  -Number of Partition\t:",len(wmi_pointer.Win32_DiskDriveToDiskPartition(["Dependent"]))
	print "  -Number of Drive\t:", len(wmi_pointer.Win32_LogicalDiskToPartition(["Dependent"]))
	print "\n*Storage_detail"
	print "  -Storage"
	for i in range(0, len(wmi_pointer.Win32_DiskDrive(["Caption"]))):
		print "     #Disk[",i,"] ", wmi_pointer.Win32_DiskDrive(["Caption"])[i].Caption
		print "        Size\t\t:",int((wmi_pointer.Win32_DiskDrive(["Size"])[i].Size))/1024/1024/1024, "GByte"
		print "        Serial Number\t:",wmi_pointer.Win32_DiskDrive(["SerialNumber"])[i].SerialNumber.strip()
		for j in range(0, wmi_pointer.Win32_DiskDrive(["Partitions"])[i].Partitions):
			drive_name=""
			try:
				drive_name=wmi_pointer.Win32_DiskDrive()[i].associators("Win32_DiskDriveToDiskPartition")[j].associators("Win32_LogicalDiskToPartition")[0].Caption
			except:
				pass
			print "              Disk[",i,"] Partition[",j,"], Drive[",drive_name,"]"
	print "  -Logical Drive"		
	for i in range(0, len(wmi_pointer.Win32_LogicalDisk())):
		print "     #Drive[", wmi_pointer.Win32_LogicalDisk()[i].DeviceID,"]\n        size:", int(wmi_pointer.Win32_LogicalDisk()[i].size)/1024/1024/1024, "GByte"

def main():
	
	wmi_pointer = wmi.WMI()
	get_process_info(wmi_pointer)
	
	

if __name__== "__main__":
	main()
	
