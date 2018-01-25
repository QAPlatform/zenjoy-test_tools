{Router} = require 'express'
logger = require('log4js').getLogger 'qa_api'
{Session, Profile} = require '../models'

SUCCESS_RET = (data) -> {errno: 0, errmsg: 'success', data}

router = Router()

# update session
router.post '/session/update', (req, res, next) ->
  {playerId, g, gv, abtests} = req.body
  Session.update {_id: playerId}, {$set: {g, gv, abtests}}, (err) ->
    return next err if err?
    next SUCCESS_RET()

# get profile
router.get '/profile/:playerId', (req, res, next) ->
  {playerId} = req.params
  
  Profile.findOne {_id: playerId}, (err, profile) ->
    return next err if err?
    return next new Error("playerId=#{playerId} not exists") unless profile
    next SUCCESS_RET(profile.data)

# replace profile
router.put '/profile/:playerId', (req, res, next) ->
  return next new Error 'api available only in development environment' unless env is 'development'
  {playerId} = req.params
  data = req.body

  Profile.update {_id: playerId}, {$set: {data}}, (err) ->
    return next err if err?
    next SUCCESS_RET()

# patch profile delta
router.patch '/profile/:playerId', (req, res, next) ->
  {playerId} = req.params
  data = req.body

  update = {}
  update["data.#{k}"] = v for k, v of data
  
  Profile.update {_id: playerId}, {$set: update}, (err) ->
    return next err if err?
    next SUCCESS_RET()

# delete profile
router.delete '/profile/:playerId', (req, res, next) ->
  {playerId} = req.params
  Profile.remove {_id: playerId}, (err, result) ->
    return next err if err?
    next SUCCESS_RET()

module.exports = router