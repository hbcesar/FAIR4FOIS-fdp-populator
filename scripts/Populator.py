import FDPClient
import Config
import Utils
from template_readers import FDPTemplateReader
import uuid
import sys


class Populator:
    """
    Class contents methods to extract content from the input CSV files and methods to populate FDP with content.
    """
    FDP_CLIENT = FDPClient.FDPClient(Config.FDP_URL, Config.FDP_USERNAME, Config.FDP_PASSWORD,
                                     Config.FDP_PERSISTENT_URL)
    UTILS = Utils.Utils()

    def __init__(self):
        """
        This __init__ method exacts datasets and distribution objects from the input CSV files. These objects are used to
        create metadata entries in the FAIR Data Point.
        """
        type = sys.argv[1]
        print(type)

        match type:
            case "semantic-artefact":
                print("Bixo doido")
                self.create_semantic_artefact()
            case "dataset":
                print("datasets")
                self.create_datasets()
            case "research-resource":
                print("rr")
            case _:
                print("No/Incorrect arguments passed")
                exit(1)
        print('tchau')


    def create_semantic_artefact(self):
         if Config.SEMANTIC_ARTEFACT_INPUT_FILE != None and Config.DISTRIBUTION_INPUT_FILE != None:
            # Get SA and distribution data
            fdp_template_reader = FDPTemplateReader.FDPTemplateReader()
            semantic_artefacts = fdp_template_reader.get_semantic_artefacts()
            distributions = fdp_template_reader.get_distributions()

            # Populate FDP with datasets
            for semantic_artefact_name, semantic_artefact in semantic_artefacts.items():
                semantic_artefact_url = self.create_resource(semantic_artefact, "sema")
                self.create_distributions(distributions, semantic_artefact_name, semantic_artefact_url)
    
    
    def create_datasets(self):
        if Config.DATASET_INPUT_FILE != None and Config.DISTRIBUTION_INPUT_FILE != None:
            # Get dataset and distribution data
            fdp_template_reader = FDPTemplateReader.FDPTemplateReader()
            datasets = fdp_template_reader.get_datasets()
            distributions = fdp_template_reader.get_distributions()

            print("Las distros:", distributions)

            # Populate FDP with datasets
            for dataset_name, dataset in datasets.items():
                dataset_url = self.create_resource(dataset, "dataset")
                self.create_distributions(distributions, dataset_name, dataset_url)

    def create_research_resource(self):
         if Config.SEMANTIC_ARTEFACT_INPUT_FILE != None and Config.DISTRIBUTION_INPUT_FILE != None:
            # Get SA and distribution data
            fdp_template_reader = FDPTemplateReader.FDPTemplateReader()
            semantic_artefacts = fdp_template_reader.get_semantic_artefacts()
            distributions = fdp_template_reader.get_distributions()

            # Populate FDP with datasets
            for semantic_artefact_name, semantic_artefact in semantic_artefacts.items():
                semantic_artefact_url = self.create_resource(semantic_artefact, "sema")
                self.create_distributions(distributions, semantic_artefact_name, semantic_artefact_url)

    
    def create_distributions(self, distributions, dataset_name, dataset_url):
        # Populate FDP with distribution(s) as child to dataset
        for distribution_name, distribution in distributions.items():
            if distribution.DATASET_NAME == dataset_name:
                distribution.PARENT_URL = dataset_url

                # This logic is required since both download and access URLs are captured in same row
                download_url = distribution.DOWNLOAD_URL
                distribution_name = distribution.TITLE
                if distribution.ACCESS_URL:
                    distribution.TITLE = "Access distribution of : " + distribution_name
                    distribution.DOWNLOAD_URL = None
                    self.create_resource(distribution, "distribution")

                if download_url:
                    distribution.TITLE = "Downloadable distribution of : " + distribution_name
                    distribution.ACCESS_URL = None
                    distribution.DOWNLOAD_URL = download_url
                    self.create_resource(distribution, "distribution")
    
    def create_resource(self, resource, resource_type):
        """
        Method to create resource of resource type in FDP

        :param dataset: Provide resource object
        :param resource_type: Provide the type of resource
        :return: FDP's dataset URL
        """
        # Check if parent exists
        parent_url = resource.PARENT_URL

        if not Config.DRY_RUN and not self.FDP_CLIENT.does_metadata_exists(parent_url):
            raise SystemExit("The parent metadata <"+parent_url+"> does not exist. Provide valid catalog URL")

        print("The catalog <"+parent_url+"> exist")

        # Obtain graph that should be sent to FDP
        graph = resource.get_graph()

        # Serialize graph and send to FDP
        post_body = graph.serialize(format='turtle')
        print("Sending the following RDF to FDP:")
        print(post_body)
        if Config.DRY_RUN:
            resource_url = "http://example.org/" + resource_type + "/" + str(uuid.uuid4())
        else:
            resource_url = self.FDP_CLIENT.fdp_create_metadata(post_body, resource_type)
        print("New " + resource_type + " created: " + resource_url)
        return resource_url