from resource_classes import Dataset
import Utils
import chevron
from rdflib import Graph

class SemantiArtefact(Dataset.Dataset):
    """
    This class extends Resource class with properties specific to dataset properties
    """
    ALT_NAME = None
    ARTEFACT_TYPE = None
    ONTOLOGY_LEVEL = None
    DEVELOPMENT_CONTEXT = []
    ONTOLOGY_PURPOSE = []

    def __init__(self, parent_url, title, description, version, language, license, issued, contributors, 
                 landing_page, keywords, acronym, alt_name, art_type, ont_level, dev_context, ont_purpose):
        """

        :param parent_url: Parent's catalog URL of a dataset. NOTE this url should exist in an FDP
        :param title: Title of a dataset
        :param description: Description of a dataset
        :param keywords: Keywords to describe a dataset
        :param themes: Themes URLs to describe a dataset
        :param publisher: Publisher URL of a dataset (e.g. https://orcid.org/0000-0002-1215-167X)
        :param language: Language URL of a dataset (e.g. http://id.loc.gov/vocabulary/iso639-1/en)
        :param license: License URL of a resource (e.g. http://rdflicense.appspot.com/rdflicense/cc-by-nc-nd3.0)
        :param page: Landing page URL of a dataset
        :param contact_point: Contact point URL or mailto URL of a dataset
        """
        # Pass core properties to parent class
        super().__init__(parent_url, title, description, version, language, license, issued, contributors, 
                         landing_page, keywords, acronym, None, None, None)
        self.ALT_NAME = alt_name
        self.ARTEFACT_TYPE = art_type
        self.ONTOLOGY_LEVEL = ont_level
        self.DEVELOPMENT_CONTEXT = dev_context
        self.ONTOLOGY_PURPOSE = ont_purpose
    
    def get_graph(self):
        """
        Method to get dataset RDF

        :return: dataset RDF
        """
        self.UTILS = Utils.Utils()
        graph = Graph()

        graph = super.get_graph(self)

        #TODO: alt name, art type, onto level, dev context, onto purpose

        return graph