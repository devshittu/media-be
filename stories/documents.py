import logging
from django_elasticsearch_dsl import Document, fields
from django_elasticsearch_dsl.registries import registry
from .models import Story

# Set up the logger for this module
logger = logging.getLogger('app_logger')


@registry.register_document
class StoryDocument(Document):
    slug = fields.TextField(
        attr='slug',  # Use the 'slug' attribute from the model
        fielddata=True,  # This allows sorting and aggregations on the field
    )
    user = fields.ObjectField(properties={
        'id': fields.IntegerField(),
        'username': fields.TextField(),
    })

    category = fields.ObjectField(properties={
        'id': fields.IntegerField(),
        'title': fields.TextField(  # Add ngram and suggest to category title
            fields={
                'suggest': fields.CompletionField(),  # For autocomplete based on category
                # Ngram search on category
                'ngram': fields.TextField(analyzer='ngram_analyzer')
            }
        ),
    })

    parent_story = fields.ObjectField(properties={
        'id': fields.IntegerField(),
        'title': fields.TextField(),
    })

    # Declare the title field once, with subfields for custom analysis
    title = fields.TextField(
        analyzer='custom_text_analyzer',  # Use this analyzer for full-text search
        fields={
            'suggest': fields.CompletionField(),  # Subfield for autocomplete
            # Subfield for ngram search
            'ngram': fields.TextField(analyzer='ngram_analyzer')
        }
    )

    # body = fields.TextField(analyzer='custom_text_analyzer')

    body = fields.TextField(
        analyzer='custom_text_analyzer',
        fields={
            # For ngram search in body
            'ngram': fields.TextField(analyzer='ngram_analyzer')
        }
    )

    class Index:
        # Name of the Elasticsearch index
        name = 'stories'
        settings = {
            'number_of_shards': 1,
            'number_of_replicas': 0,
            'index.max_ngram_diff': 7,  # Allow difference of 7 (10 - 3)
            'analysis': {
                'analyzer': {
                    'custom_text_analyzer': {
                        'type': 'custom',
                        'tokenizer': 'standard',
                        'filter': [
                            'lowercase',  # Lowercase all terms
                            'stop',       # Remove stopwords
                            'porter_stem',  # Stem words using the Porter algorithm
                        ],
                    },
                    'ngram_analyzer': {  # Ngram analyzer for autocomplete and partial matches
                        'type': 'custom',
                        'tokenizer': 'standard',
                        'filter': ['lowercase', 'ngram_filter']
                    }
                },
                'filter': {
                    'ngram_filter': {  # Ngram filter for autocomplete
                        'type': 'ngram',
                        'min_gram': 3,
                        'max_gram': 10
                    },
                    'porter_stem': {
                        'type': 'stemmer',
                        'name': 'porter'
                    },
                    'stop': {
                        'type': 'stop',
                        'stopwords': '_english_'
                    }
                }
            }
        }

    class Django:
        model = Story
        fields = [
            'source_link',
            'event_occurred_at',
            'event_reported_at',
        ]
        # Additional fields that may require custom mapping
        ignore_signals = False
        auto_refresh = True
        queryset_pagination = 5000

    def save(self, **kwargs):
        logger.debug(
            f"Indexing document for story: {self.instance.id} - {self.instance.title}")
        result = super().save(**kwargs)
        logger.debug(
            f"Successfully indexed document for story: {self.instance.id}")
        return result

    def delete(self, **kwargs):
        logger.debug(f"Deleting document for story: {self.instance.id}")
        result = super().delete(**kwargs)
        logger.debug(
            f"Successfully deleted document for story: {self.instance.id}")
        return result


# stories/documents.py
