from resource_classes import Resource
import Utils
import chevron
from rdflib import Graph

class ResearchResource(Resource.Resource):
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

    IDENTIFIER = None

    def __init__(self, parent_url, title, description, version, language, license, issued, contributors, 
                 landing_page, keywords, acronym, frequency = None, temp_coverage = None, temp_resolution = None, identifier):
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
        super().__init__(parent_url, title, description, version, language, license, issued)
        self.CONTRIBUTORS = contributors
        self.LANDING_PAGE = landing_page
        self.KEYWORDS = keywords
        self.ACRONYM = acronym
        
        self.FREQUENCY = frequency
        self.TEMPORAL_COVERAGE = temp_coverage
        self.TEMPORAL_RESOLUTION = temp_resolution

        self.IDENTIFIER = identifier
    
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
        #     with open('../templates/landingpage.mustache', 'r') as f:
        #         body = chevron.render(f, {'page_url': self.LANDING_PAGE})
        #         graph.parse(data=body, format="turtle")
        self.UTILS.add_landing_page(self, graph)

        # Create keywords list
        keyword_str = ""
        for keyword in self.KEYWORDS:
            keyword_str = keyword_str + ' "' + keyword + '",'
        keyword_str = keyword_str[:-1]

        # Create themes list
        # theme_str = ""
        # for theme in self.THEMES:
        #     theme_str = theme_str + " <" + theme + ">,"
        # theme_str = theme_str[:-1]

        #Create contributors list
        contributors_str = ""
        for contributor in self.CONTRIBUTORS:
            contributors_str = contributors_str + '<' + contributor + '>, '
        contributors_str = contributors_str[:-1]
            

        # create dataset triples
        with open('../templates/research_resource.mustache', 'r') as f:
            body = chevron.render(f, {'keyword': keyword_str, 'contributor': contributors_str, 'acronym': self.ACRONYM,
                                      'identifier': self.IDENTIFIER})
            graph.parse(data=body, format="turtle")

        return graph