BOT_NAME = 'data_collectors'

SPIDER_MODULES = ['data_collectors.spiders']
NEWSPIDER_MODULE = 'data_collectors.spiders'

# Configure item pipelines
ITEM_PIPELINES = {
   'data_collectors.pipelines.DataCollectorsPipeline': 300,
}
