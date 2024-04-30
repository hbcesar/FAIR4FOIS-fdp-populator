from resource_classes import Dataset
import Utils
import chevron
from rdflib import Graph

class SemanticArtefact(Dataset.Dataset):
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
        #  # create resource triples
        # self.UTILS.add_resource_triples(self, graph)
        # # Create language triples
        # self.UTILS.add_language_triples(self, graph)
        # # Create license triples
        # self.UTILS.add_licence_triples(self, graph)

        # # Create landing page triples
        # # if self.LANDING_PAGE:
        # with open('../templates/landingpage.mustache', 'r') as f:
        #     body = chevron.render(f, {'page_url': self.LANDING_PAGE})
        #     graph.parse(data=body, format="turtle")
        # self.UTILS.add_landing_page(self, graph)

        # # Create keywords list
        # keyword_str = ""
        # for keyword in self.KEYWORDS:
        #     keyword_str = keyword_str + ' "' + keyword + '",'
        # keyword_str = keyword_str[:-1]
        # print(keyword_str)

        # #Create contributors list
        # contributors_str = ""
        # for contributor in self.CONTRIBUTORS:
        #     contributors_str = contributors_str + ' <' + contributor + '>,'
        # contributors_str = contributors_str[:-1]

        # create s_a triples
        with open('../templates/semantic_artefact.mustache', 'r') as f:
            body = chevron.render(f, {'keyword': keyword_str, 'contributor': contributors_str, 'acronym': self.ACRONYM,
                                      'art_type': self.ARTEFACT_TYPE, 'purpose': self.ONTOLOGY_PURPOSE,
                                       'context': self.DEVELOPMENT_CONTEXT, 'domain': self.ONTOLOGY_LEVEL })
            graph.parse(data=body, format="turtle")

        return graph