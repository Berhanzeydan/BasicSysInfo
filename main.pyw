import psutil
import platform
from datetime import datetime
import GPUtil
from PyQt5 import QtCore, QtWidgets
import cpuinfo

def get_size(bytes, suffix="B"):
    """
    Scale bytes to its proper format
    e.g:
        1253656 => '1.20MB'
        1253656678 => '1.17GB'
    """
    factor = 1024
    for unit in ["", "K", "M", "G", "T", "P"]:
        if bytes < factor:
            return f"{bytes:.2f}{unit}{suffix}"
        bytes /= factor


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(797, 781)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.DiskInfo = QtWidgets.QLabel(self.centralwidget)
        self.DiskInfo.setObjectName("DiskInfo")
        self.gridLayout_2.addWidget(self.DiskInfo, 4, 0, 1, 1)
        self.Bilgi = QtWidgets.QLabel(self.centralwidget)
        self.Bilgi.setObjectName("Bilgi")
        self.gridLayout_2.addWidget(self.Bilgi, 6, 1, 1, 1)
        self.GPUDet = QtWidgets.QLabel(self.centralwidget)
        self.GPUDet.setObjectName("GPUDet")
        self.gridLayout_2.addWidget(self.GPUDet, 6, 0, 1, 1)
        self.NetworkInfo = QtWidgets.QLabel(self.centralwidget)
        self.NetworkInfo.setObjectName("NetworkInfo")
        self.gridLayout_2.addWidget(self.NetworkInfo, 4, 1, 1, 1)
        self.CPU = QtWidgets.QLabel(self.centralwidget)
        self.CPU.setObjectName("CPU")
        self.gridLayout_2.addWidget(self.CPU, 3, 0, 1, 1)
        self.Memory = QtWidgets.QLabel(self.centralwidget)
        self.Memory.setObjectName("Memory")
        self.gridLayout_2.addWidget(self.Memory, 3, 1, 1, 1)
        self.Boot = QtWidgets.QLabel(self.centralwidget)
        self.Boot.setObjectName("Boot")
        self.gridLayout_2.addWidget(self.Boot, 1, 1, 1, 1)
        self.SysInfo = QtWidgets.QLabel(self.centralwidget)
        self.SysInfo.setObjectName("SysInfo")
        self.gridLayout_2.addWidget(self.SysInfo, 1, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 797, 21))
        self.menubar.setObjectName("menubar")
        self.menuDosya = QtWidgets.QMenu(self.menubar)
        self.menuDosya.setObjectName("menuDosya")
        MainWindow.setMenuBar(self.menubar)
        self.actionYenile = QtWidgets.QAction(MainWindow)
        self.actionYenile.setObjectName("actionYenile")
        self.menuDosya.addAction(self.actionYenile)
        self.menubar.addAction(self.menuDosya.menuAction())
        MainWindow.setStyleSheet("background-color: #dae8fd;")
        self.SysInfo.setStyleSheet("border: 1px solid #000000; border-radius: 6px; padding: 10px;")
        self.CPU.setStyleSheet("border: 1px solid #000000; border-radius: 6px; padding: 10px;")
        self.DiskInfo.setStyleSheet("border: 1px solid #000000; border-radius: 6px; padding: 10px;")
        self.Memory.setStyleSheet("border: 1px solid #000000; border-radius: 6px; padding: 10px;")
        self.GPUDet.setStyleSheet("border: 1px solid #000000; border-radius: 6px; padding: 10px;")
        self.Boot.setStyleSheet("border: 1px solid #000000; border-radius: 6px; padding: 10px;")
        self.Bilgi.setStyleSheet("border: 1px solid #000000; border-radius: 6px; padding: 10px; ")
        self.NetworkInfo.setStyleSheet("border: 1px solid #000000; border-radius: 6px; padding: 10px;")
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        self.actionYenile.triggered.connect(self.getSysInfo)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Sistem Bilgisi Aracı"))
        self.DiskInfo.setText(_translate("MainWindow", "Disk Bilgisi"))
        self.Bilgi.setText(_translate("MainWindow", "\nMithat Berhan Zeydan"))
        self.GPUDet.setText(_translate("MainWindow", "GPU Detail"))
        self.NetworkInfo.setText(_translate("MainWindow", "Ağ Bilgisi"))
        self.CPU.setText(_translate("MainWindow", "İşlemci Bilgisi"))
        self.Memory.setText(_translate("MainWindow", "Bellek Bilgisi"))
        self.Boot.setText(_translate("MainWindow", ""))
        self.SysInfo.setText(_translate("MainWindow", "Sistem Bilgisi"))
        self.menuDosya.setTitle(_translate("MainWindow", "Araçlar"))
        self.actionYenile.setText(_translate("MainWindow", "Yenile"))

    def getSysInfo(self):
        self.CPU.setText(self.getCPU())
        self.Memory.setText(self.getMemory())
        self.DiskInfo.setText(self.getDisks())
        self.NetworkInfo.setText(self.getNetwork())
        bt = datetime.fromtimestamp(psutil.boot_time())
        self.Boot.setText(f"Son Önyükleme Zamanı: {bt.hour}:{bt.minute}:{bt.second} {bt.day}/{bt.month}/{bt.year}")
        self.GPUDet.setText(self.getGPU())
        self.SysInfo.setText(self.getSystem())
    
    def getCPU(self):
        cpufreq = psutil.cpu_freq()
        return f"{cpuinfo.get_cpu_info()['brand_raw']}\n\nÇekirdek Sayısı: {psutil.cpu_count(logical=False)}\nToplam İş Parçacığı Sayısı: {psutil.cpu_count(logical=True)}\nMaksimum Frekans: {cpufreq.max:.2f}MHz\nMinimum Frekansı: {cpufreq.min:.2f}MHz\nGüncel Frekans: {cpufreq.current:.2f}MHz\nToplam CPU Kullanımı: {psutil.cpu_percent()}%"

    def getMemory(self):
        svmem = psutil.virtual_memory()
        swap = psutil.swap_memory()
        return f"Toplam RAM: {get_size(svmem.total)}\nKullanılabilir RAM: {get_size(svmem.available)}\nKullanılan RAM: {get_size(svmem.used)}\nRAM Kullanımı: %{svmem.percent}\n\nToplam Sanal Bellek: {get_size(swap.total)}\nKullanılabilir Sanal Bellek: {get_size(swap.free)}\nKullanılan Sanal Bellek: {get_size(swap.used)}\nKullanılan Sanal Bellek Yüzdesi: {swap.percent}%"

    def getDisks(self):
        partitions = psutil.disk_partitions()
        disk_io = psutil.disk_io_counters()
        disks = []
        for partition in partitions:
            try:
                partition_usage = psutil.disk_usage(partition.mountpoint)
            except PermissionError:
                continue
            disks.append(f"Disk: {partition.device}\nDisk Dosya Formatı: {partition.fstype}\nToplam Alanı: {get_size(partition_usage.total)}\nKullanılan Disk Alanı: {get_size(partition_usage.used)}\nBoştaki Disk Alanı: {get_size(partition_usage.free)}\nDisk Doluluk Oranı: {partition_usage.percent}%\nToplam Disk Okuması: {get_size(disk_io.read_bytes)}\nToplam Disk Yazması: {get_size(disk_io.write_bytes)}")
        return "\n\n".join(disks)

    def getNetwork(self):
        if_addrs = psutil.net_if_addrs()
        net_io = psutil.net_io_counters()
        interfaces = []
        for interface_name, interface_addresses in if_addrs.items():
            for address in interface_addresses:
                if str(address.family) == 'AddressFamily.AF_INET':
                    interfaces.append(f"{interface_name}:\nIP Adresi: {address.address}\nAğ Maskesi: {address.netmask}\nYayın IP Adresi: {address.broadcast if address.broadcast is not None else 'Bulunamadı'}\n")
                elif str(address.family) == 'AddressFamily.AF_PACKET':
                    interfaces.append(f"{interface_name}:\nMAC Adresi: {address.address}\nAğ Maskesi: {address.netmask}\nYayın MAC Adresi: {address.broadcast if address.broadcast is not None else 'Bulunamadı'}\n")
        return "\n\n".join(interfaces) + f"\nToplam Alınan Ağ: {get_size(net_io.bytes_recv)}\nToplam Gönderilen Ağ: {get_size(net_io.bytes_sent)}"

    def getGPU(self):
        gpus = [f"GPU Adı: {gpu.name}\nGPU Kullanımı: {gpu.load*100}%\nKullanılabilir GPU Belleği: {gpu.memoryFree}MB\nKullanılan GPU Belleği: {gpu.memoryUsed}MB\nToplam GPU Belleği: {gpu.memoryTotal}MB\nGPU Temperature: {gpu.temperature} °C" for gpu in GPUtil.getGPUs()]
        return "\n\n".join(gpus) if len(gpus) > 0 else "Harici GPU Bulunamadı. 😥"

    def getSystem(self):
        uname = platform.uname()
        return f"OS: {uname.system}\nSistem İsmi: {uname.node}\nOS Çekirdek Sürümü {uname.release}\nOS Sürümü: {uname.version}\nMakine Mimarisi: {uname.machine}"


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    ui.getSysInfo()
    MainWindow.show()
    sys.exit(app.exec_())
