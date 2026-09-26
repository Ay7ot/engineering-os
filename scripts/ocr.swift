#!/usr/bin/env swift
// EngineeringOS OCR helper.
// Extracts text from an image using the macOS Vision framework (no extra deps).
// Usage: swift ~/EngineeringOS/scripts/ocr.swift <image-path>
// Exit codes: 0 = text extracted and printed to stdout; 1 = failure; 3 = no text detected.
import Foundation
import Vision
import AppKit

let args = CommandLine.arguments
guard args.count >= 2 else {
    FileHandle.standardError.write(Data("usage: ocr.swift <image-path>\n".utf8))
    exit(2)
}

let path = args[1]
guard let img = NSImage(contentsOfFile: path) else {
    FileHandle.standardError.write(Data("ocr: could not load image at \(path)\n".utf8))
    exit(1)
}

var rect = NSRect(origin: .zero, size: img.size)
guard let cg = img.cgImage(forProposedRect: &rect, context: nil, hints: nil) else {
    FileHandle.standardError.write(Data("ocr: could not rasterize image\n".utf8))
    exit(1)
}

let request = VNRecognizeTextRequest()
request.recognitionLevel = .accurate
request.usesLanguageCorrection = true

let handler = VNImageRequestHandler(cgImage: cg, options: [:])
do {
    try handler.perform([request])
    let lines = (request.results ?? []).compactMap { $0.topCandidates(1).first?.string }
    if lines.isEmpty {
        FileHandle.standardError.write(Data("ocr: no text detected in image\n".utf8))
        exit(3)
    }
    print(lines.joined(separator: "\n"))
} catch {
    FileHandle.standardError.write(Data("ocr: \(error)\n".utf8))
    exit(1)
}