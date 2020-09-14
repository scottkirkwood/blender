// Package main creates one image from many
package main

import (
	"flag"
	"fmt"
	"image"
	"image/draw"
	"image/png"
	"os"
	"path/filepath"
	"sort"
)

var (
	outputFlag      = flag.String("o", "", "Ouput filename (required)")
	expectEqualFlag = flag.Bool("expect-equal", true, "Expect each image to be the same size")
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

func readImages(filenames []string) (images []image.Image, err error) {
	for _, filename := range filenames {
		reader, err := os.Open(filename)
		if err != nil {
			return nil, err
		}
		image, err := png.Decode(reader)
		reader.Close()
		if err != nil {
			return nil, err
		}
		images = append(images, image)
	}
	return images, nil
}

// grabImages grabs the filenames from args.
// We glob all args and then sort the results lexicographically.
func grabImages(args []string) ([]image.Image, error) {
	fnames := make([]string, 0, len(args))
	for _, glob := range args {
		more, err := filepath.Glob(glob)
		if err != nil {
			return nil, err
		}
		fnames = append(fnames, more...)
	}
	fnames = sort.StringSlice(fnames)
	return readImages(fnames)
}

func checkSizes(images []image.Image, expectEqualFlag bool) error {
	var w, h int

	for i, image := range images {
		b := image.Bounds()
		if i > 0 {
			if w != b.Dx() || h != b.Dy() {
				return fmt.Errorf("image $%d is %dx%d expected %dx%d", i, b.Dx(), b.Dy(), w, h)
			}
		}
		w, h = b.Dx(), b.Dy()
	}
	return nil
}

func fail(format string, args ...interface{}) {
	fmt.Fprintf(os.Stderr, format, args)
	os.Exit(-1)
}

func main() {
	flag.Parse()

	if *outputFlag == "" {
		fail("Need -o output filename")
	}

	images, err := grabImages(flag.Args())
	if err != nil {
		fail("Unable to read images %v\n", err)
	}
	err = checkSizes(images, *expectEqualFlag)
	if err != nil {
		fail("Images sizes different %v\n", err)
	}
	err = combineImagesHorizontally(images, *outputFlag)
	if err != nil {
		fail("Unable to merge images %v\n", err)
	}
}
