"use strict";
const vscode = require("vscode");
const languageclient = require("vscode-languageclient");

let client;

function activate(context) {
    try {
        const serverOptions = {
            command: ".venv/bin/gdoc",
            args: [
                "language-server",
                "--logging-filename",
                ".gdoc-language-server.log",
                "--logging-filemode",
                "a",
                "--logging-level",
                "DEBUG",
                "--logging-timestamp",
            ],
            options: {
                cwd: vscode.workspace.workspaceFolders ? vscode.workspace.workspaceFolders[0].uri.fsPath : undefined
            }
        };
        // const serverOptions = function () {
        //     return new Promise((resolve, reject) => {
        //         const socket = net.connect({ port: 6009, host: "localhost" });
        //         socket.on("connect", () => {
        //             resolve({
        //                 reader: socket,
        //                 writer: socket,
        //             });
        //         });
        //         socket.on("error", (err) => {
        //             reject(err);
        //         });
        //     });
        // };
        const clientOptions = {
            documentSelector: [
                {
                    scheme: "file",
                    language: "markdown",
                },
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
