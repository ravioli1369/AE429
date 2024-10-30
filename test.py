from bs4 import BeautifulSoup
import pandas as pd

# URL of the HTML file (replace with the actual URL if available)
url = "Properties_of_Standard_Atmosphere.html"

# Read the HTML content
with open(url, "r") as file:
    html_content = file.read()

# Parse the HTML content using BeautifulSoup
soup = BeautifulSoup(html_content, "html.parser")

# Find the specific table based on the header text
table = None
for tbl in soup.find_all("table"):
    if tbl.find("th", text="MSISE-90 Model of Earth's Upper Atmosphere"):
        table = tbl
        break

# Check if the table was found
if table is None:
    raise ValueError("Table not found")

# Initialize lists to store the altitude and density data
altitudes = []
densities = []

# Iterate over each row and extract the altitude and density data
for row in table.find_all("tr")[2:]:  # Skip the header rows
    cells = row.find_all("td")
    if len(cells) >= 4:
        altitude = cells[0].text.strip()
        density = cells[6].text.strip()
        altitudes.append(altitude)
        densities.append(density)

# Convert the lists to a DataFrame
data = pd.DataFrame({"Altitude(km)": altitudes, "Density(kg/m^3)": densities})

# Print the DataFrame
print(data)

data.to_csv("atmosphere_data.csv", index=False)
