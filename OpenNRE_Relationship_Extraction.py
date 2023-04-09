import opennre

# download NRE pretrained model
model = opennre.get_model('wiki80_cnn_softmax')

# text used to look for relations
text = """
Kobe Bean Bryant was an American professional basketball player.
A shooting guard, he spent his entire career with the Los Angeles Lakers in the NBA.
"""

# choose two entities whose relation is to be predicted
h_text = "Kobe Bean Bryant"
t_text = "shooting guard"
h_pos = (text.index(h_text), text.index(h_text) + len(h_text))
t_pos = (text.index(t_text), text.index(t_text) + len(t_text))

# predict relation
model.infer({'text': text, 'h': {'pos': h_pos}, 't': {'pos': t_pos}})

# output:
# ('position played on team / speciality', 0.9829357862472534)