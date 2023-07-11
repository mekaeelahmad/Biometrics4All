  simpleQuotes.py takes in customer information including their business name, first/last name, phone number, and address and updates it. simpleQuotes.py outputs the given information in a specific format whilst fixes incorrect inputs. For example, it outputs the customer's number in the format "(XXX) XXX-XXXX" and updates the user's address using a python file called addressUpdate.py in the parent folder which I also wrote. addressUpdate.py takes a user's address as an input and outputs the correctly formatted/corrected address using Google's Maps API. 




  googleLocations.py uses the "Store Hours" column in the sheet "hours" in the excel file Locations.xlsx in order to update it's 7 different columns representing the timings for reach respective day starting from Sunday. This issue revolves around inconsistent formats and several edge cases for entries in the "Store Hours" column that represent when businesses partnered with Biometrics4ALL conduct their businesses. 

  These edge cases consist of the following formats: format2 =  “FirstDay-LastDay: FirstTime-LastTime”. FirstDay and LastDay can follow the following abbreviations: Su, M, T, W, Th, F, Sa. FirstTime and LastTime can follow the following formats: HHAM, HAM, H:MMAM, HHPM, HPM, H:MMPM. It is not case sensitive. For example, if an entry in “Store Hours” looked like “M-F:9AM-12PM” this means that for that row, the Monday, Tuesday, Wednesday, Thursday and Friday columns would show 9AM-12PM translated into the form HH:MMAM-HH:MMPM or “09:00AM-12:00PM”. Saturday and Sunday should be blank. 

  Additionally, there could be multiple times for format2, it could be “FirstDay-LastDay: FirstTime-LastTime, FirstTime-LastTime, …” which means there are multiple times that follow for those consecutive days. This would be an example: “M-F:9AM-12PM, 1:30PM-5:30PM”. We would need to format this like “HH:MMAM-HH:MMPM, HH:MMAM-HH:MMPM” so it would show “09:00AM-12:00PM, 01:30PM-5:30PM” for that entry. 

  The data can also be formatted with the following format: 
format3 = “FirstDay, SecondDay, …, LastDay: FirstTime-LastTime”
This would mean that the days aren’t consecutive, but follow the same times. All the days would have the same abbreviations like Su, M, T, W, Th, F, Sa for Sunday, Monday, Tuesday, Wednesday, Thursday, and Friday.  Additionally, there could be multiple times for days just as there was for the previous format. 

  Finally, some data cells in the “Store Hours” column could include multiple of these formats followed by a new line. For example, it could include something like: 
“format2format3” which would look like “M-Th:9am-7pmF:9am-5pm”. As you can see there is a time for Friday, but there is no new line between the two formats and this is a single input. So if there are multiple different formats in a single input, googleLocations.py would update the store hours for those days. It could look like “format2format2format2format3” or “format3format2format2” and so on. There are varying combinations of format2 and format3. 

  Ultimately, googleLocations.py parses through each business hours in "Store Hours" in order to properly update 7 seperate columns to represent the business's hours in a format that follows Google's Business Spreadsheet of 
HH:MMAM-HH:MMPM for each day. 

