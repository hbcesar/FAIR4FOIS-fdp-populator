from resource_classes import Resource
import Utils
import chevron
from rdflib import Graph

class Dataset(Resource.Resource):
    """
    This class extends Resource class with properties specific to dataset properties
    """
    CONTRIBUTORS = []
    LANDING_PAGE = None
    KEYWORDS = []
    ACRONYM = None
    
    FREQUENCY = None
    TEMPORAL_COVERAGE = None
    TEMPORAL_RESOLUTION = None

    def __init__(self, parent_url, title, description, version, language, license, issued, contributors, 
                 landing_page, keywords, acronym, frequency = None, temp_coverage = None, temp_resolution = None):
        # Pass core properties to parent class
        super().__init__(parent_url, title, description, version, language, license, issued)

        self.CONTRIBUTORS = contributors
        self.LANDING_PAGE = landing_page
        self.KEYWORDS = keywords
        self.ACRONYM = acronym
        
        self.FREQUENCY = frequency
        self.TEMPORAL_COVERAGE = temp_coverage
        self.TEMPORAL_RESOLUTION = temp_resolution
    
    def get_graph(self):
        """
        Method to get dataset RDF

        :return: dataset RDF
        """
        self.UTILS = Utils.Utils()
        graph = Graph()

        # create resource triples
        self.UTILS.add_resource_triples(self, graph)
        # Create language triples
        self.UTILS.add_language_triples(self, graph)
        # Create license triples
        self.UTILS.add_licence_triples(self, graph)

        # Create landing page triples
        # if self.LANDING_PAGE:
        with open('../templates/landingpage.mustache', 'r') as f:
            body = chevron.render(f, {'page_url': self.LANDING_PAGE})
            graph.parse(data=body, format="turtle")
        # self.UTILS.add_landing_page(self, graph)

        # Create keywords list
        keyword_str = ""
        for keyword in self.KEYWORDS:
            keyword_str = keyword_str + ' "' + keyword + '",'
        keyword_str = keyword_str[:-1]
        print(keyword_str)

        #Create contributors list
        contributors_str = ""
        for contributor in self.CONTRIBUTORS:
            contributors_str = contributors_str + ' <' + contributor + '>,'
        contributors_str = contributors_str[:-1]
            
        # create dataset triples
        with open('../templates/dataset.mustache', 'r') as f:
            body = chevron.render(f, {'keyword': keyword_str, 'contributor': contributors_str, 'acronym': self.ACRONYM})
            graph.parse(data=body, format="turtle")

        #TODO: frequency, temporal, temporal

        return graph