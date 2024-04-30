import Config
import csv
from resource_classes import Dataset, Distribution
# import Utils
from datetime import datetime

DATASET_NAME = None
LANGUAGE = None

class FDPTemplateReader:
    """
    NOTE: this class is based on the folling specification:
    <https://github.com/LUMC-BioSemantics/EJP-RD-WP19-FDP-template>
    """
    def get_datasets(self):
        """
        This method creates datasets objects by extracting content from the dataset input CSV file.
        NOTE: This method assumes that provided input file follows this spec
        <https://github.com/LUMC-BioSemantics/EJP-RD-WP19-FDP-template>

        :return: Dict of datasets
        """

        reader = csv.reader(open(Config.DATASET_INPUT_FILE, 'r'), delimiter=";")
        catalog_url = Config.CATALOG_URL
        datasets = {}
        for row in reader:
            if reader.line_num > 1 and row[0] != "":
                title = row[0]
                description = row[1]
                contributors = row [2]
                license = row[3]
                issued = row[4]
                landing_page_url = row[5]
                keywords_str = row[6]
                acronym = row[7]
                language = row[8]
                version = row[9]

                self.DATASET_NAME = title
                self.LANGUAGE = language

                if not description:
                    description = "Metadata of dataset " + title
                # Create language triples
                # if language:
                #     language_url = "http://id.loc.gov/vocabulary/iso639-1/" + language.strip()
                
                # Create license triples
                # if license:
                #     license_url = license.strip()
               
               # Create landing page triples
                if landing_page_url:
                    landing_page_url = landing_page_url.strip()
                
                # Create keywords list
                keywords = []
                for keyword in keywords_str.split(","):
                    keyword = keyword.strip()
                    keywords.append(keyword)
                
                # Creates contributors list
                contributors_list = []
                for contributor in contributors.split(","):
                    contributor = contributor.strip()
                    contributors_list.append(contributor)

                #Adjust issued
                issued = self.adjust_issued(issued)

                dataset = Dataset.Dataset(catalog_url, title, description, version, language, 
                                          license, issued, contributors_list, landing_page_url, keywords, acronym)
                datasets[title] = dataset
        return datasets

    def get_distributions(self):
        """
        This method creates distribution objects by extracting content from the distribution input CSV file.
        NOTE: This method assumes that provided input file follows this spec
        <https://github.com/LUMC-BioSemantics/EJP-RD-WP19-FDP-template>

        :return: Dict of distribution
        """

        reader = csv.reader(open(Config.DISTRIBUTION_INPUT_FILE, 'r'), delimiter=";")
        distributions = {}
        for row in reader:
            if reader.line_num > 2 and row[0] != "":
                print(row)
                title = row[0]
                version = row[1]
                description = row[2]
                issued = row[3]
                license = row[4]
                access_url = row[5]
                download_url = row[6]
                media_type = row[7]

                if not description:
                    description = "Metadata of distribution " + title
                # Create language triples
                # if language:
                #     language_url = "http://id.loc.gov/vocabulary/iso639-1/" + language.strip()
                # Create license triples
                
                if license:
                    license = license.strip()

                issued = self.adjust_issued(issued)
                distribution = Distribution.Distribution(None, title, description, version, 
                                                         self.LANGUAGE, license, issued, access_url, download_url, media_type, self.DATASET_NAME)
                distributions[title] = distribution
        return distributions
    

    def adjust_issued(self, issued):
        issued = datetime.strptime(issued, "%Y-%m-%d")
        issued_format = "{year:d}-{month:02d}-{day:02d}"
        issued = '"' + issued_format.format(year = issued.year, month = issued.month, day = issued.day) + 'T00:00:00Z"^^xsd:dateTime'

        return issued