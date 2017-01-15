from flask import Flask, make_response, request, render_template
import io
import csv

app = Flask(__name__)

def transform(text_file_contents):
    return text_file_contents.replace("=", ",")


@app.route('/')
def form():
    return render_template('index.html')

@app.route('/transform', methods=["POST"])
def transform_view():
    f1 = request.files['datafile_one']
    f2 = request.files['datafile_two']

    if not f1:
        return "No file 1"

    if not f2:
        return "No file 2"

    stream1 = io.StringIO(f1.stream.read().decode("UTF8"), newline=None)
    csv_input_1 = csv.reader(stream1)

    stream2 = io.StringIO(f2.stream.read().decode("UTF8"), newline=None)
    csv_input_2 = csv.reader(stream2)
    #print("file contents: ", file_contents)
    #print(type(file_contents))
    # print(csv_input)
    # for row in csv_input:
    #     print(row)
    return render_template('output.html',
    csv_input_1=csv_input_1,
    csv_input_2=csv_input_2)

    # stream.seek(0)
    # result = transform(stream.read())
    #
    # response = make_response(result)
    # response.headers["Content-Disposition"] = "attachment; filename=result.csv"
    # return response

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5001, debug=True)
