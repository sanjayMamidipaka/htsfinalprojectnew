from flask import Flask, render_template, request
from enigma.rotors.rotor import Rotor
from enigma.plugboard import Plugboard
from enigma.machine import EnigmaMachine
import rsa
app = Flask(__name__)

@app.route('/')
def index():
  return render_template('index.html')

@app.route('/my-link/', methods=['POST', 'GET'])
def my_link():

    try:
      output = request.form.to_dict()
      print(output)
      name = output["name"]
      rotors = output['rotor1'] + " " + output['rotor2'] + " " + output['rotor3']
      reflectorString = output['reflector']
      print(rotors)

      machine = EnigmaMachine.from_key_sheet(
      rotors=rotors,
      reflector=reflectorString,
      ring_settings='B U L',
      plugboard_settings='AV BS CG DL FU HZ IN KM OW RX')

      machine.set_display('WXC') # set initial rotor positions
      enc_key = machine.process_text('BLA') # encrypt message key

      machine.set_display('BLA') # use message key BLA
      ciphertext = machine.process_text(name)

      machine.set_display('WXC')
      msg_key = machine.process_text(enc_key)

      machine.set_display(msg_key) # original message key is BLA
      plaintext = machine.process_text(ciphertext)

      return render_template('index.html', ciphertext=ciphertext, plaintext=plaintext)
    except Exception:
      return render_template('index.html', ciphertext="ERROR! PLEASE TRY AGAIN! (MAKE SURE TO SELECT ALL INPUTS)", plaintext="")

@app.route('/my-link-new/', methods=['POST', 'GET'])
def my_link_new():
  try:
    output = request.form.to_dict()
    name1 = output['name1']
    publicKey, privateKey = rsa.newkeys(256)
    message = name1
    encMessage = rsa.encrypt(message.encode(), publicKey)

    decMessage = rsa.decrypt(encMessage, privateKey).decode()

    return render_template('index.html', publicKey=publicKey, privateKey=privateKey, encMessage=encMessage, decMessage=decMessage)
  except Exception:
    return render_template('index.html', publicKey="ERROR! PLEASE TRY AGAIN! (MAKE SURE INPUT IS UNDER 22 CHARACTERS)", privateKey="", encMessage="", decMessage="")
if __name__ == '__main__':
  app.run(debug=True)