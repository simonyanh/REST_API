from flask import Flask, jsonify
from flask_restful import Resource, Api, reqparse
import pandas as pd
import numpy as np

app = Flask(__name__)
api = Api(app)


class Bugs(Resource):

    def get(self):  # to view a specific bug by title
        parser = reqparse.RequestParser()
        parser.add_argument('title', required=True)
        args = parser.parse_args()

        data = pd.read_csv('bugs.csv')
        selected_data = data.loc[data['title'] == args['title']]
        selected_data = selected_data.to_dict(orient='records')
        return {'bug': selected_data}, 200

    def post(self):  # to add a new bug
        parser = reqparse.RequestParser()
        parser.add_argument('title', required=True)
        parser.add_argument('body', required=True)
        parser.add_argument('status', required=True)
        args = parser.parse_args()

        data = pd.read_csv('bugs.csv')

        if args['title'] in list(data['title']):
            return {
                       'message': f"'{args['title']}' already exists."
                   }, 409
        else:
            new_data = pd.DataFrame({
                'title': [args['title']],
                'body': [args['body']],
                'status': [args['status']],
            })

            data = data.append(new_data, ignore_index=True)
            data.to_csv('bugs.csv', index=False)
            return {'bugs': data.to_dict()}, 200

    def patch(self):  # to edit a bug
        parser = reqparse.RequestParser()
        parser.add_argument('title', required=True)
        parser.add_argument('newtitle', store_missing=False)
        parser.add_argument('body', store_missing=False)
        parser.add_argument('status', store_missing=False)
        args = parser.parse_args()

        data = pd.read_csv('bugs.csv')

        if args['title'] in list(data['title']):

            if 'body' in args:
                data.loc[data['title'] == args['title'], 'body'] = args['body']

            if 'status' in args:
                data.loc[data['title'] == args['title'], 'status'] = args['status']

            if 'newtitle' in args:
                if args['newtitle'] in list(data['title']):
                    return {
                               'message': f"'{args['newtitle']}' already exists."
                           }, 409
                data.loc[data['title'] == args['title'], 'title'] = args['newtitle']

            data.to_csv('bugs.csv', index=False)
            return {'bug': data.to_dict()}, 200

        else:
            return {
                       'message': f"'{args['title']}' bug not found."
                   }, 404

    def delete(self):  # to delete a bug by title
        parser = reqparse.RequestParser()
        parser.add_argument('title', required=True)
        args = parser.parse_args()

        data = pd.read_csv('bugs.csv')

        if args['title'] in list(data['title']):
            data = data[data['title'] != args['title']]

            data.to_csv('bugs.csv', index=False)
            return {'data': data.to_dict()}, 200
        else:
            return {
                       'message': f"'{args['title']}' bug not found."
                   }, 404


class Comments(Resource):

    def put(self):  # to add a new comment
        parser = reqparse.RequestParser()
        parser.add_argument('title', required=True)
        parser.add_argument('commenttitle', required=True)
        parser.add_argument('comment', required=True)
        args = parser.parse_args()

        data = pd.read_csv('bugs.csv')

        if args['title'] in list(data['title']):
            data.loc[data['title'] == args['title'], 'commentTitle'] = args['commenttitle']
            data.loc[data['title'] == args['title'], 'comment'] = args['comment']

            data.to_csv('bugs.csv', index=False)
            return {'bugs': data.to_dict()}, 200
        else:
            return {
                       'message': f"'{args['title']}' bug not found."
                   }, 404

    def delete(self):  # to delete a comment by title
        parser = reqparse.RequestParser()
        parser.add_argument('title', required=True)
        args = parser.parse_args()

        data = pd.read_csv('bugs.csv')

        if args['title'] in list(data['title']):
            data.loc[data['title'] == args['title'], ['commentTitle', 'comment']] = np.nan

            data.to_csv('bugs.csv', index=False)
            return {'data': data.to_dict()}, 200
        else:
            return {
                       'message': f"'{args['title']}' bug not found."
                   }, 404


class User(Resource):
    def put(self):  # to assign the bug to a user
        parser = reqparse.RequestParser()
        parser.add_argument('title', required=True)
        parser.add_argument('userid', required=True)
        args = parser.parse_args()

        data = pd.read_csv('bugs.csv')

        if args['title'] in list(data['title']):
            data.loc[data['title'] == args['title'], 'assigned_userID'] = args['userid']

            data.to_csv('bugs.csv', index=False)
            return {'bugs': data.to_dict()}, 200
        else:
            return {
                       'message': f"'{args['title']}' bug not found."
                   }, 404

@app.route('/allbugs', methods=['GET'])  # view all bugs (without comments)
def allbugs():
    data = pd.read_csv('bugs.csv')
    data = data.loc[:, ['title', 'body', 'status']].to_dict()
    return {'bugs': data}, 200


@app.route('/allbugs/resolved', methods=['GET'])  # view all resolved bugs
def resolvedbugs():
    data = pd.read_csv('bugs.csv')
    data = data.loc[data['status'] == 'resolved', ['title', 'body', 'status']].to_dict()
    return {'bugs': data}, 200


api.add_resource(Bugs, '/bugs')
api.add_resource(Comments, '/comment')
api.add_resource(User, '/assign')

if __name__ == '__main__':
    app.run()
