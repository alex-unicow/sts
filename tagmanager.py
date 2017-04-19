from bottle import post, get, put, delete
import re, json, sqlite3
from bottle import request, response
from pprint import pprint


tagpattern = re.compile(r'^[a-zA-Z \.\-\d]{1,64}$')



@get('/tag/<tag_id>')
def show_tag(tag_id):

    #ensure id is an integer

    try:
       conn = sqlite3.connect('tag.db')
       c = conn.cursor()
       c.execute('SELECT id, name, create_datetime FROM tags where id=?',(tag_id,))
       row = c.fetchone()
       
       if row is None:
          raise KeyError

    except Exception as e:
       raise e
    except KeyError:
        response.status = 404
        return

    finally:
       conn.close()

    
    response.headers['Content-Type'] = 'application/json'
    response.headers['Cache-Control'] = 'no-cache'

    tag = { 'id': row[0], 'name': row[1], 'created': row[2] }

    return json.dumps({'tag': tag})
    
    
@get('/object/<object_id>')
def show_object(object_id):

    #todo: ensure id is an integer
    #todo: if not found 404
    #todo: proper return json

    try:
       conn = sqlite3.connect('tag.db')
       c = conn.cursor()
       c.execute('SELECT id, name, create_datetime FROM objects where id=?',(object_id,))
       row = c.fetchone()
       
       if row is None:
          raise KeyError

    except Exception as e:
       raise e
    except KeyError:
        response.status = 404
        return

    finally:
       conn.close()

    
    response.headers['Content-Type'] = 'application/json'
    response.headers['Cache-Control'] = 'no-cache'

    object = { 'id': row[0], 'name': row[1], 'created': row[2] }
    return json.dumps({'object': object})


@get('/tags')
def list_tags():
    try:
       conn = sqlite3.connect('tag.db')
       c = conn.cursor()
       c.execute('SELECT id,name,create_datetime FROM tags')
       rows = c.fetchall()

    except Exception as e:
       print("exception")
       raise e
    finally:
       conn.close()

    response.headers['Content-Type'] = 'application/json'
    response.headers['Cache-Control'] = 'no-cache'

    all_tags = []
    for row in rows: 
        tag = { 'id': row[0], 'name': row[1], 'created': row[2] }
        all_tags.append(tag)

    return json.dumps({'tags': all_tags})


@get('/objects')
def list_objects():
    try:
       conn = sqlite3.connect('tag.db')
       c = conn.cursor()
       c.execute('SELECT id,name,create_datetime FROM objects')
       rows = c.fetchall()

    except Exception as e:
       print("exception")
       raise e
    finally:
       conn.close()

    response.headers['Content-Type'] = 'application/json'
    response.headers['Cache-Control'] = 'no-cache'

    all_objects = []
    for row in rows:
        object = { 'id': row[0], 'name': row[1], 'created': row[2] }
        all_objects.append(object)

    return json.dumps({'objects': all_objects})



@post('/tags')
def create_tag():
    try:
        # parse input data
        try:
            data = request.json
        except:
           raise ValueError

        if data is None:
            raise ValueError

        # extract and validate name
        try:
            if tagpattern.match(data['tag']) is None:
                raise ValueError
            tag = data['tag']
        except (TypeError, KeyError):
            raise ValueError


    except ValueError:
        # if bad request data, return 400 Bad Request
        response.status = 400
        return
    
    except KeyError:
        # if name already exists, return 409 Conflict
        response.status = 409
        return

    # add tag
    try:
       conn = sqlite3.connect('tag.db')
       c = conn.cursor()
       c.execute("INSERT INTO tags (name,create_datetime) VALUES (?,datetime('now'))",(tag,))
       conn.commit()
    except Exception as e:
       conn.rollback()
       raise e
    finally:
       conn.close()
    
    # return 200 Success
    # TODO should return the actual new tag, not just the name
    response.headers['Content-Type'] = 'application/json'
    return json.dumps({'tag': tag})



@post('/objects')
def create_object():
    try:
        # parse input data
        try:
            data = request.json
        except:
           raise ValueError

        if data is None:
            raise ValueError

        # extract and validate name
        try:
            if tagpattern.match(data['object']) is None:
                raise ValueError
            object = data['object']
        except (TypeError, KeyError):
            raise ValueError


    except ValueError:
        # if bad request data, return 400 Bad Request
        response.status = 400
        return
    
    except KeyError:
        # if name already exists, return 409 Conflict
        response.status = 409
        return

    # add tag
    try:
       conn = sqlite3.connect('tag.db')
       c = conn.cursor()
       c.execute("INSERT INTO objects (name,create_datetime) VALUES (?,datetime('now'))",(object,))
       conn.commit()
    except Exception as e:
       conn.rollback()
       raise e
    finally:
       conn.close()
    
    # return 200 Success
    # TODO should return the actual new tag, not just the name
    response.headers['Content-Type'] = 'application/json'
    return json.dumps({'object': object})







@delete('/object/<object_id>')
def delete_object(object_id):
    '''deletes object'''

    try:
       conn = sqlite3.connect('tag.db')
       c = conn.cursor()
       c.execute('SELECT * FROM objects where id=?',(object_id,))
       object = c.fetchone()

       if object is None:
          raise KeyError
      
       data = c.execute('DELETE FROM objects where id=?',(object_id,))
       conn.commit()

    except Exception as e:
       raise e
    except KeyError:
        response.status = 404
        return

    finally:
       conn.close()


    response.headers['Cache-Control'] = 'no-cache'
    response.status = 200
    return


@delete('/tag/<tag_id>')
def delete_tag(tag_id):
    '''deletes tag'''

    try:
       conn = sqlite3.connect('tag.db')
       c = conn.cursor()
       c.execute('SELECT * FROM tags where id=?',(tag_id,))
       tag = c.fetchone()

       if tag is None:
          raise KeyError
      
       data = c.execute('DELETE FROM tags where id=?',(tag_id,))
       conn.commit()

    except Exception as e:
       raise e
    except KeyError:
        response.status = 404
        return

    finally:
       conn.close()


    response.headers['Cache-Control'] = 'no-cache'
    response.status = 200
    return






@put('/tag/<tag_id>')
def update_tag(tag_id):
    '''update tag'''
    
    
    # parse input data
    try:
        data = request.json
    except:
        raise ValueError

    if data is None:
        raise ValueError

    # extract and validate name
    try:
        if tagpattern.match(data['name']) is None:
            raise ValueError
        name = data['name']
    except (TypeError, KeyError):
        raise ValueError

    try:
       conn = sqlite3.connect('tag.db')
       c = conn.cursor()
       c.execute('SELECT * FROM tags where id=?',(tag_id,))
       tag = c.fetchone()

       if tag is None:
          raise KeyError
      
       data = c.execute('UPDATE tags set name=? where id=?',(name,tag_id,))
       conn.commit()

    except Exception as e:
       raise e
    except KeyError:
        response.status = 404
        return

    finally:
       conn.close()


    response.headers['Cache-Control'] = 'no-cache'
    response.headers['Content-Type'] = 'application/json'
    return json.dumps({'tag': tag})



@put('/object/<object_id>')
def update_object(object_id):
    '''update object'''
    
    # parse input data
    try:
        data = request.json
    except:
        raise ValueError

    if data is None:
        raise ValueError

    # extract and validate name
    try:
        if tagpattern.match(data['name']) is None:
            raise ValueError
        name = data['name']
    except (TypeError, KeyError):
        raise ValueError


    try:
       conn = sqlite3.connect('tag.db')
       c = conn.cursor()
       c.execute('SELECT * FROM objects where id=?',(object_id,))
       object = c.fetchone()

       if object is None:
          raise KeyError
      
       data = c.execute('UPDATE objects set name=? where id=?',(name,object_id,))
       conn.commit()

    except Exception as e:
       raise e
    except KeyError:
        response.status = 404
        return

    finally:
       conn.close()


    response.headers['Cache-Control'] = 'no-cache'
    response.headers['Content-Type'] = 'application/json'
    return json.dumps({'object': object})



@get('/tags/search_results')
def search_tags():
    try:
        if 'q' not in request.query:
            raise KeyError
        query = request.query.q
    except KeyError:
        response.status = 400
        return
    
    try:
       conn = sqlite3.connect('tag.db')
       c = conn.cursor()
       c.execute('SELECT id,name,create_datetime FROM tags where name LIKE ?',('%'+query+'%',))
       rows = c.fetchall()

    except Exception as e:
       raise e
    finally:
       conn.close()


    response.headers['Cache-Control'] = 'no-cache'
    response.headers['Content-Type'] = 'application/json'

    all_tags = []
    for row in rows:
        tag = { 'id': row[0], 'name': row[1], 'created': row[2] }
        all_tags.append(tag)

    return json.dumps({'tags': all_tags})


@get('/objects/search_results')
def search_objects():
    try:
        if 'q' not in request.query:
            raise KeyError
        query = request.query.q
    except KeyError:
        response.status = 400
        return
    
    try:
       conn = sqlite3.connect('tag.db')
       c = conn.cursor()
       c.execute('SELECT id,name,create_datetime FROM objects where name LIKE ?',('%'+query+'%',))
       rows = c.fetchall()
    except Exception as e:
       raise e
    finally:
       conn.close()


    response.headers['Cache-Control'] = 'no-cache'
    response.headers['Content-Type'] = 'application/json'

    all_objects = []
    for row in rows:
        object = { 'id': row[0], 'name': row[1], 'created': row[2] }
        all_objects.append(object)
    return json.dumps({'objects': all_objects})



@get('/object/<object_id>/tags')
def list_tags_for_object(object_id):

    try:
       conn = sqlite3.connect('tag.db')
       c = conn.cursor()
       c.execute('SELECT tags.id, tags.name, tags.create_datetime FROM tags JOIN object_tag ON tags.id = object_tag.tag_id where object_tag.object_id=?',(object_id,))
       rows = c.fetchall()

    except Exception as e:
       raise e

    finally:
       conn.close()


    response.headers['Content-Type'] = 'application/json'
    response.headers['Cache-Control'] = 'no-cache'

    all_tags = []
    for row in rows:
        tag = { 'id': row[0], 'name': row[1], 'created': row[2] }
        all_tags.append(tag)
    return json.dumps({'tags': all_tags})



@get('/tag/<tag_id>/objects')
def list_objects_for_tag(tag_id):

    try:
       conn = sqlite3.connect('tag.db')
       c = conn.cursor()
       c.execute('SELECT objects.id, objects.name, objects.create_datetime FROM objects JOIN object_tag ON objects.id = object_tag.object_id where object_tag.tag_id=?',(tag_id,))
       rows = c.fetchall()

    except Exception as e:
       raise e

    finally:
       conn.close()

    response.headers['Content-Type'] = 'application/json'
    response.headers['Cache-Control'] = 'no-cache'

    all_objects = []
    for row in rows:
        object = { 'id': row[0], 'name': row[1], 'created': row[2] }
        all_objects.append(object)
    return json.dumps({'objects': all_objects})


@get('/tags/<tag_ids>/objects')
def list_objects_for_tags(tag_ids):

    num_tags = len(tag_ids.split(","))
  
    print(num_tags)

    try:
       conn = sqlite3.connect('tag.db')
       c = conn.cursor()
       c.execute('SELECT objects.id, objects.name, objects.create_datetime FROM objects JOIN (select object_tag.object_id from object_tag where object_tag.tag_id in ('+tag_ids+') group by object_tag.object_id having count(object_tag.object_id) >= ?) as object_tags ON  object_tags.object_id = objects.id',(num_tags,))

       rows = c.fetchall()

    except Exception as e:
       raise e

    finally:
       conn.close()

    response.headers['Content-Type'] = 'application/json'
    response.headers['Cache-Control'] = 'no-cache'

    all_objects = []
    for row in rows:
        object = { 'id': row[0], 'name': row[1], 'created': row[2] }
        all_objects.append(object)
    return json.dumps({'objects': all_objects})



@put('/object/<object_id>/tag/<tag_id>')
def tag_object(object_id,tag_id):
    try:
       conn = sqlite3.connect('tag.db')
       c = conn.cursor()
       c.execute("INSERT INTO object_tag (object_id,tag_id,create_datetime) VALUES (?,?,datetime('now'))",(object_id,tag_id,))
       conn.commit()
    except Exception as e:
       conn.rollback()
       raise e
    finally:
       conn.close()

    # return 200 Success
    response.status = 200
    response.headers['Content-Type'] = 'application/json'
    return json.dumps({'tag_id': tag_id})



@delete('/object/<object_id>/tag/<tag_id>')
def untag_object(object_id,tag_id):
        
    try:
       conn = sqlite3.connect('tag.db')
       c = conn.cursor()
       c.execute('SELECT * FROM object_tag where object_id=? and tag_id=?',(object_id,tag_id,))
       object_tag = c.fetchone()

       if object_tag is None:
          raise KeyError

       data = c.execute('DELETE FROM object_tag where object_id=? and tag_id=?',(object_id,tag_id,))
       conn.commit()

    except Exception as e:
       raise e
    except KeyError:
        response.status = 404
        return

    finally:
       conn.close()

    response.headers['Cache-Control'] = 'no-cache'
    response.status = 200
    return


