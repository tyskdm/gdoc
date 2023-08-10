"use strict";
const vscode = require("vscode");
const languageclient = require("vscode-languageclient");

let client;

function activate(context) {
    try {
        const serverOptions = {
            // command: "node",
            // args: [
            //     context.extensionPath + "/gdoc.js",
            //     "--language-server"
            // ]
            // command: "python3",
            // args: [
            //     "-m",
            //     context.extensionPath + "/gdoc",
            //     "language-server",
            //     "--help",
            // ]
            command: context.extensionPath + "/bin/gdoc",
            args: [
                "language-server",
                "--logging-filename",
                context.extensionPath + "/.gdoc-language-server.log",
                "--logging-level",
                "WARNING",
            ]
        };
        const clientOptions = {
            documentSelector: [
                {
                    scheme: "file",
                    language: "gdoc",
                }
            ],
        };
        client = new languageclient.LanguageClient("gdoc", serverOptions, clientOptions);
        context.subscriptions.push(client.start());
    } catch (e) {
        vscode.window.showErrorMessage("gdoc-language-server couldn't be started.");
    }
}

function deactivate() {
    if (client) return client.stop();
}

module.exports = { activate, deactivate }
