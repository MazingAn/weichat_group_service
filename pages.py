import jinja2
import settings

TemplateLoader = jinja2.FileSystemLoader(searchpath='./templates')
TemplateEnv = jinja2.Environment(loader=TemplateLoader)
template = TemplateEnv.get_template('template.html') 

def render_records(time_span, records):
	out_file = settings.SERVER_ROOT + 'index.html'
	page_source = template.render(time_span=time_span, rows=records)
	with open(out_file, 'w') as f:
		f.write(page_source)
