package controllers

import javax.inject.Inject

import play.api.mvc._

// Controller that handles file upload

class FileUploadController @Inject()(cc: ControllerComponents) extends AbstractController(cc) {

    def upload = Action(parse.temporaryFile) { request =>
        request.body.moveTo(Paths.get("/tmp/picture/uploaded"), replace = true)
        Ok("File uploaded")
}