// Package main creates one image from many
package main

import (
	"flag"
	"fmt"
	"image"
	"image/draw"
	"image/png"
	"io/ioutil"
	"os"
	"os/exec"
	"path"
	"regexp"
	"strings"
)

var (
	outputFlag = flag.String("o", "", "Ouput filename (required)")
)

func combineImagesHorizontally(images []image.Image, outputFilename string) error {
	width, height := 0, 0
	for _, image := range images {
		b := image.Bounds()
		width += b.Dx()
		if b.Dy() > height {
			height = b.Dy()
		}
	}
	m := image.NewRGBA(image.Rect(0, 0, width, height))

	x := 0
	for _, curImage := range images {
		b := curImage.Bounds()
		r := image.Rect(x, 0, x+b.Dx(), b.Dy())
		draw.Draw(m, r, curImage, image.ZP, draw.Src)
		x += b.Dx()
	}
	writer, err := os.Create(outputFilename)
	if err != nil {
		return err
	}
	defer writer.Close()
	return png.Encode(writer, m)
}

func main() {

}
