import requests as rq
import csv
import bs4
import random

proxies = [{ip strings of your proxies.}]

def get_proxy():
    return proxies[random.randrange(0, len(proxies))]

def get_os(osUrl, deviceDict):
    osPage = rq.get("http://phonedb.net/" + osUrl)
    soup = bs4.BeautifulSoup(osPage.text, "lxml")
    table = soup.find("table")
    for tr in table.findAll("tr"):
        tds = tr.findAll("td")
        if len(tds) == 2:
            strong = tds[0].find("strong")
            plain_text = tds[1].text
            if strong is not None:
                column = str(strong.text)
                if(column == "Codename"):
                    deviceDict["OS Codename"] = plain_text.replace("\n", "")
                if(column == "Description"):
                    deviceDict["OS Description"] = plain_text.replace("\n", "").replace("\r", "").replace("\xa0››", "")
                if(column == "Released"):
                    deviceDict["Release Year"] = plain_text.replace("\n", "")
                else:
                    deviceDict[column] = plain_text.replace("\n", "")

def get_cpu(cpuUrl, deviceDict):
    cpuPage = rq.get("http://phonedb.net/" + cpuUrl)
    soup = bs4.BeautifulSoup(cpuPage.text, "lxml")
    table = soup.find("table")
    
    for tr in table.findAll("tr"):
        tds = tr.findAll("td")
        if len(tds) == 2:
            strong = tds[0].find("strong")
            plain_text = tds[1].text
            if strong is not None:
                column = str(strong.text)
                if(column == "Codename"):
                    deviceDict["CPU Codename"] = plain_text.replace("\n", "").replace("\r", "").replace("\xa0››", "")
                else:
                    deviceDict[column] = plain_text.replace("\n", "").replace("\r", "").replace("\xa0››", "")

def get_device(deviceUrl, deviceNumber):
    deviceDict = {}
    devicePage = rq.get(r"http://phonedb.net/"  + deviceUrl)
    soup = bs4.BeautifulSoup(devicePage.text, "lxml")
    table = soup.find("table")

    for tr in table.findAll("tr"):
        tds = tr.findAll("td")
        if len(tds) == 2:
            strong = tds[0].find("strong")
            plain_text = tds[1].text
            if strong is not None:
                column = str(strong.text)
                if(column == "Supported Cellular Data Links" or column == "Complementary GPS Services" or column ==  "Supported BeiDou system (BDS)"):
                    pass
                if(column == "Operating System"):
                    deviceDict[column] = plain_text.replace("\n", "")
                    if "^" not in tds[1].findAll("a")[1].get("href"):
                        get_os(tds[1].findAll("a")[1].get("href"), deviceDict)
                    print("------DEVICE" + str(deviceNumber) + " OS info gathered")
                if(column == "CPU"):
                    deviceDict[column] = plain_text.replace("\n", "").replace("\r", "").replace("\xa0››", "")
                    get_cpu(tds[1].findAll("a")[1].get("href"), deviceDict)
                    print("------DEVICE" + str(deviceNumber) + " CPU info gathered")
                else:
                    deviceDict[column] = plain_text.replace("\n", "").replace("\r", "").replace("\xa0››", "")
    return deviceDict



with open('phonedb.csv', 'a', newline='', encoding='utf-8') as csv_file:
    field_names = ['Brief', 'Brand', 'Model', 'Released', 'Announced', 'Hardware Designer', 'Manufacturer', 'Codename', 'General Extras', 'Device Category', 'Width', 'Height', 'Depth', 'Mass', 'Operating System', 'Developer', 'Full Name', 'Release Year', 'OS Codename', 'Short Name', 'Operating System Kernel', 'Operating System Family', 'Supported CPU Instruction Set(s)', 'OS Description', 'CPU Clock', 'CPU', 'Designer', 'Type', 'CPU Codename', 'Year Released', 'Function', 'Width of Machine Word', 'Supported Instruction Set(s)', 'Type of processor core(s)', 'Number of processor core(s)', 'Memory Interface(s)', 'Max. Clock Frequency of Memory IF', 'Data Bus Width', 'Number of data bus channels', 'Max. Data Rate', 'Recommended Maximum Clock Frequency', 'L1 Instruction Cache per Core', 'L1 Data Cache per Core', 'Total L2 Cache', 'Total L3 Cache', 'Feature Size', 'Semiconductor Technology', 'Fab', 'Embedded GPU', 'GPU Clock', 'Supported Cellular Data Links', 'Supported GPS protocol(s)', 'Supported Galileo service(s)', 'Supported GLONASS protocol(s)', 'Supported BeiDou system (BDS)', 'RAM Type', 'RAM Capacity (converted)', 'Non-volatile Memory Capacity (converted)', 'Display Diagonal', 'Resolution', 'Horizontal Full Bezel Width', 'Display Area Utilization', 'Pixel Density', 'Display Type', 'Number of Display Scales', 'Display Refresh Rate', 'Scratch Resistant Screen', 'A/V Out', 'Microphone(s)', 'Loudpeaker(s)', 'Audio Output', 'Supported Cellular Bands', 'SIM Card Slot', 'Complementary Phone Services', 'Dual Cellular Network Operation', 'Sec. Supported Cellular Networks', 'Sec. Supported Cellular Data Links', 'Sec. SIM Card Slot', 'Touchscreen Type', 'Expansion Interfaces', 'USB', 'Bluetooth', 'Wireless LAN', 'NFC', 'FM Radio Receiver', 'Camera Placement', 'Camera Image Sensor', 'Image Sensor Pixel Size', 'Number of effective pixels', 'Aperture (W)', 'Zoom', 'Focus', 'Min. Equiv. Focal Length', 'Video Recording', 'Flash', 'Camera Extra Functions', 'Aux. Camera Image Sensor', 'Aux. Cam. Image Sensor Pixel Size', 'Auxiliary Camera Resolution', 'Aux. Camera Aperture (W)', 'Aux. Camera Extra Functions', 'Aux. 2 Camera Image Sensor', 'Auxiliary 2 Camera Resolution', 'Aux. 2 Camera Aperture (W)', 'Aux. 3 Camera Image Sensor', 'Aux.4 Camera Image Sensor', 'Secondary Camera Placement', 'Secondary Camera Sensor', 'Secondary Number of pixels', 'Secondary Aperture (W)', 'Secondary Video Recording', 'Secondary Camera Extra Functions', 'Sec. Aux. Cam. Image Sensor', 'Built-in compass', 'Built-in accelerometer', 'Built-in gyroscope', 'Additional sensors', 'Protection from solid materials', 'Protection from liquids', 'Immersion into liquids (depth limit)', 'Immersion into liquids time limit', 'Battery', 'Battery Cells in Parallel', 'Nominal Battery Voltage', 'Nominal Battery Capacity', 'Nominal Battery Energy', 'Talk Time', 'Wireless Charging', 'Market Countries', 'Market Regions']
    csv_writer = csv.DictWriter(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL, fieldnames=field_names)
    csv_writer.writeheader()
    nextPageUrl = "index.php?m=device&s=list&filter=16295"
    deviceNumber = 16294
    pageNumber = 1
    
    while nextPageUrl is not None:
        page = rq.get("http://phonedb.net/" + nextPageUrl)
        soup = bs4.BeautifulSoup(page.text, "lxml")
        nextPage = soup.find('a', {'title':'Next page'})
        deviceLinks = soup.findAll("div",{'class':"content_block_title"})
        
        for deviceLink in deviceLinks:
            resultSet = get_device(deviceLink.find("a").get("href").replace("^", "\^"), deviceNumber)
            print("------DEVICE" + str(deviceNumber) + " info gathered")
            deviceNumber = deviceNumber + 1

            device = {}
            for key in resultSet:
                if key in field_names:
                    device[key] = resultSet[key]
            csv_writer.writerow(device)
        
        print("------PAGE #" + str(pageNumber) + " is ready")
        
        pageNumber = pageNumber + 1
        
        if nextPage is not None:
            nextPageUrl = nextPage.get("href")
        else:
            nextPageUrl = None

